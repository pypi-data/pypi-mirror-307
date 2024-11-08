"""LLM related functions."""
import base64
import json

from vertexai.generative_models import GenerationConfig, GenerativeModel, Part

from src.tms_formatting import get_formatted_value
from src.utils import get_data_set_schema, get_processor_name

model_gen, model_config = None, None


response_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "skuData": {
                "type": "object",
                "properties": {
                    "grossWeight": {"type": "string"},
                    "hsCode": {"type": "string"},
                    "measurements": {"type": "string"},
                    "netWeight": {"type": "string"},
                    "packagingType": {"type": "string"},
                    "quantityShipped": {"type": "string"},
                    "skuDescription": {"type": "string"},
                    "skuNumbers": {"type": "string"},
                    "poNumber": {"type": "string"},
                    "poPosition": {"type": "string"},
                    "containerNumber": {"type": "string"},
                    "sealNumber": {"type": "string"},
                },
            }
        },
    },
}


"""Prompt for the task"""


PROMPT = """
You are tasked with extracting specific data points from a document related to logistic and freight forwarding.
Each data point is part of a master field called skuData.
There may be multiple skuData entries in a document. Your goal is to extract all instances.


        grossWeight: Total weight of the cargo, including the tare weight of the container.
        hsCode: Harmonized System code for classifying products for customs.
        measurements: Dimensions of the cargo (length, width, height) for freight calculations.
        netWeight: Weight of the goods excluding packaging and containers.
        packagingType: Type of packaging used (e.g., cartons, pallets, barrels).
        quantityShipped: Quantity of goods, prioritize larger packaging types (Pallets > Cartons > Pieces).
        skuDescription: Description of the goods.
        skuNumbers: Unique number for the security seal on a container.
        poNumber: Purchase order number for the goods.
        poPosition: Specific line or item number in the purchase order.
        containerNumber: Unique ID for tracking the shipping container.
        sealNumber: Security seal number ensuring cargo integrity.

        Output Format:
        Extracted data should be structured as follows:

        [
            {
              "skuData": {
              "grossWeight": "",
              "hsCode": "",
              "measurements": "",
              "netWeight": "",
              "packagingType": "",
              "quantityShipped": "",
              "skuDescription": "",
              "skuNumbers": "",
              "poNumber": "",
              "poPosition": "",
              "containerNumber": "",
              "sealNumber": ""
                }
            },
            {
              "skuData": {
              "grossWeight": "",
              "hsCode": "",
              "measurements": "",
              "netWeight": "",
              "packagingType": "",
              "quantityShipped": "",
              "skuDescription": "",
              "skuNumbers": "",
              "poNumber": "",
              "poPosition": "",
              "containerNumber": "",
              "sealNumber": ""
                }
            },
            {...}
        ]

    The above example only contains two skuData entries. There may be more in the document.
    You need to extract all of them.
    If the container number, seal number, PO number or PO position are not found in the sku data,
     search in other location of the document and map it accordingly.
    After extraction, return only the extracted data in the above format excluding all other information.
    """

gemini_parameters = {
    "temperature": 0,
    "maxOutputTokens": 8000,
    "top_p": 0.8,
    "top_k": 5,
    "model_id": "gemini-1.5-flash-001",
    "response_mime_type": "application/json",
}


def initialize_gemini_for_pl(parameters: dict):
    """Ask the Gemini model a question.

    Args:
        parameters (dict): The parameters to use for the model.

    Returns:
        str: The response from the model.
    """
    if parameters is None:
        parameters = {
            "temperature": 0,
            "maxOutputTokens": 100,
            "top_p": 0.8,
            "top_k": 40,
            "model_id": "gemini-1.5-flash-001",
        }

    # Initialize the model if it is not already initialized
    model_gen = GenerativeModel(model_name=parameters["model_id"])

    # Set the generation configuration
    model_config = GenerationConfig(
        max_output_tokens=parameters["maxOutputTokens"],
        temperature=parameters["temperature"],
        top_p=parameters["top_p"],
        top_k=parameters["top_k"],
        response_mime_type=parameters["response_mime_type"],
        response_schema=response_schema,
    )

    return model_gen, model_config


def ask_gemini_pl(prompt: str, parameters: dict, document=None):
    """Ask the Gemini model a question.

    Args:
        prompt (str): The prompt to send to the model.
        parameters (dict): The parameters to use for the model.

    Returns:
        str: The response from the model.
    """
    global model_gen, model_config, model_response_text

    if model_gen is None or model_config is None:
        # Initialize the model
        model_gen, model_config = initialize_gemini_for_pl(parameters)

    if document is None:

        # Generate the response for no document
        model_response = model_gen.generate_content(
            contents=prompt, generation_config=model_config
        )
    else:
        # Generate the response with a document
        model_response = model_gen.generate_content(
            [document, prompt],
            generation_config=model_config,
            stream=False,
        )

    return model_response.text


def get_unified_json_genai_pl(prompt, parameters=None, document=None):
    """Send a prompt to a Google Cloud AI Platform model and returns the generated json.

    Args:
        prompt (str): The prompt to send to the LLM model.
        parameters (dict, optional): The parameters to use for the model. Defaults to None.

    Returns:
        dict: The generated json from the model.
    """
    # Ask the LLM model
    if document is None:
        result = ask_gemini_pl(prompt, parameters)
    else:
        result = ask_gemini_pl(prompt, parameters, document)
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        raise ValueError(
            f"Failed to decode the response from the model: \n reason: Token Limit exceeded"
        )


# Function to extract skuData properties
def extract_sku_data_properties(schema):
    """Extract the properties of skuData from the schema."""
    sku_data_properties = {}
    # Navigate through entity_types to find skuData
    for entity in schema.document_schema.entity_types:
        if entity.name == "skuData":
            for prop in entity.properties:
                # Store the property name, value_type, and occurrence_type in a dictionary
                occurrence_type_str = prop.occurrence_type.name
                sku_data_properties[prop.name] = {
                    "value_type": prop.value_type,
                    "occurrence_type": occurrence_type_str,
                }

    return sku_data_properties


# Function to get the schema of the document
async def get_modify_docAI_schema(params, schema_client, input_doc_type, isBetaTest):
    """Get the schema of the document from the Document AI processor."""
    processor_name = await get_processor_name(params, input_doc_type, isBetaTest)
    # Get the schema of a processor and select only the entity types
    schema = await get_data_set_schema(schema_client, name=processor_name)

    schema_dict = extract_sku_data_properties(schema)

    return schema_dict


def prepare_document_for_gemini(file_content):
    """Prepare a document from file content by encoding it to base64.

    Args:
        file_content (bytes): The binary content of the file to be processed.

    Returns:
        Part: A document object ready for processing by the language model.
    """
    # Convert binary file to base64
    pdf_base64 = base64.b64encode(file_content).decode("utf-8")

    # Create the document for the model
    document = Part.from_data(
        mime_type="application/pdf", data=base64.b64decode(pdf_base64)
    )

    # Split the text into words
    document_text = base64.b64decode(pdf_base64)  # Adjust decoding as necessary

    # Split the text into words
    words = document_text.split()
    print("count of words in document", len(words))

    # logger.info(f"Document contains {len(words)} words.")

    return document


async def process_file_w_llm(PROMPT, parameter, file_content):
    """Process a document using a language model (gemini) to extract structured data.

    Args:
        document (Union[Part, str]): The document object prepared for processing.
        input_doc_type (str): The type of document, used to select the appropriate prompt from the prompt library.

    Returns:
        result (dict): The structured data extracted from the document, formatted as JSON.
    """
    # TODO: change to a more dynamic struture for multiple LLM types, for now its only compatible with gemini
    # convert file_content to required document
    document = prepare_document_for_gemini(file_content)

    # generate the result with LLM (gemini)
    result = get_unified_json_genai_pl(
        prompt=PROMPT, parameters=parameter, document=document
    )

    return result


async def process_sku_data_pl(prompt, gemini_parameters, file_content, embed_manager):
    """
    Process file content using an LLM and formats SKU data.

    Args:
        prompt (str): The prompt to be used with the LLM.
        gemini_parameters (dict): Parameters for the LLM processing.
        file_content (str): The content of the file to be processed.
        embed_manager (object): An object to manage embeddings for formatted values.

    Returns:
        dict: A dictionary containing the aggregated SKU data.
    """
    # Process the file content with the LLM
    llm_response = await process_file_w_llm(prompt, gemini_parameters, file_content)

    # Initialize a list to store SKU data
    sku_data_list = []

    # Iterate over the response to process each SKU
    for sku in llm_response:
        for _, value in sku.items():
            sku_dict = {}
            for key, val in value.items():
                if val is None:
                    sku_dict.update(
                        {key: {"documentValue": val, "formattedValue": None}}
                    )
                else:
                    formatted_value = get_formatted_value(key, val, embed_manager)
                    sku_dict.update(
                        {key: {"documentValue": val, "formattedValue": formatted_value}}
                    )
            sku_data_list.append(sku_dict)

    return sku_data_list
