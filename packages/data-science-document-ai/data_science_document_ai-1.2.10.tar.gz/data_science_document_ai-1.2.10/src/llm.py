"""LLM related functions."""
import base64
import json
import re

from openai import OpenAI
from vertexai.generative_models import GenerationConfig, GenerativeModel, Part

from src.io import logger

model_gen, model_config = None, None
chatgpt_client = None

def initialize_gemini(parameters: dict):
    """Ask the Gemini model a question.

    Args:
        parameters (dict): The parameters to use for the model.

    Returns:
        str: The response from the model.
    """
    if parameters is None:
        parameters = {
            "temperature": 0,
            "maxOutputTokens": 1000,
            "top_p": 0.8,
            "top_k": 40,
            "model_id": "gemini-1.5-pro-001",
        }

    # Initialize the model if it is not already initialized
    model_gen = GenerativeModel(model_name=parameters["model_id"])

    # Set the generation configuration
    model_config = GenerationConfig(
        max_output_tokens=parameters["maxOutputTokens"],
        temperature=parameters["temperature"],
        top_p=parameters["top_p"],
        top_k=parameters["top_k"],
    )

    return model_gen, model_config


def ask_gemini(prompt: str, parameters: dict, document=None):
    """Ask the Gemini model a question.

    Args:
        prompt (str): The prompt to send to the model.
        parameters (dict): The parameters to use for the model.

    Returns:
        str: The response from the model.
    """
    global model_gen, model_config

    if model_gen is None or model_config is None:
        # Initialize the model
        model_gen, model_config = initialize_gemini(parameters)

    if document is None:

        # Generate the response
        model_response = model_gen.generate_content(
            contents=prompt, generation_config=model_config
        )
        response_text = model_response.text
    else:
        # Generate the response
        model_response = model_gen.generate_content(
            [document, prompt], generation_config=model_config, stream=True,
        )

        response_text = ""
        for response in model_response:
            response_text += response.text

    return response_text


def clean_llm_response(response):
    """Cleans the response from LLM to get a valid JSON.

    This function searches for a JSON block within a response, extracts it,
    and replaces single quotes with double quotes. It also removes newline
    characters to ensure the JSON is formatted as a single line.

    Args:
        response (str): The raw response string from LLM.

    Returns:
        str: A cleaned and formatted JSON string extracted from the response.
    """
    if "```json" in response:
        json_start = response.index("```json") + len("```json")
        json_end = response.index("```", json_start)
        response = response[json_start:json_end]
    elif "```" in response:
        json_start = response.index("```") + len("```")
        json_end = response.index("```", json_start)
        response = response[json_start:json_end]

    return response.replace("'", "\"").replace("\n", " ").replace("\\n", " ")


def clean_quotes_from_json(response):
    """Cleans unnecessary quotes from a JSON string within a response.

    This function processes a response string to remove quotes that are not
    needed for JSON keys or values, ensuring valid JSON formatting. It
    specifically targets quotes that appear around keys or structural
    elements like colons and commas.

    Args:
        response (str): The raw response string containing JSON data.

    Returns:
        cleaned_response (str): A cleaned JSON string with unnecessary quotes removed.
    """
    cleaned_list = []
    response = response.replace('{ "', '{"')
    response = response.replace('" }', '"}')
    first_ix = response.index('{"') + 1
    end_ix = response.index('{"') + 1
    for ix, char in enumerate(response[first_ix:]):
        if char == '"':
            prev_char = response[first_ix+ix-1]
            next_char = response[first_ix+ix+1]
            #if next_char.isalnum() or next_char.isspace():
            if next_char in [":", ",", "}"] or prev_char in [" ", ",", "{"]:
                start_ix = end_ix
                end_ix = ix + 2
                cleaned_list.append(response[start_ix:end_ix])
            elif next_char.isalnum() and prev_char.isalnum():
                start_ix = end_ix
                end_ix = ix + 2
                cleaned_list.append(response[start_ix:end_ix])
                end_ix += 1

    # TODO: find a more generic way to do this
    # problem is if the last valu is null
    if cleaned_list[-1] == '"vgmCutOff':
        cleaned_list.append('": null}')
        cleaned_response = '{' + "".join(cleaned_list)
    else:
        cleaned_response = '{' + "".join(cleaned_list) + '"}]}'
    return cleaned_response


def get_unified_json_genai(prompt, parameters=None, document=None):
    """Send a prompt to a Google Cloud AI Platform model and returns the generated json.

    Args:
        prompt (str): The prompt to send to the LLM model.
        parameters (dict, optional): The parameters to use for the model. Defaults to None.

    Returns:
        dict: The generated json from the model.
    """
    # Ask the LLM model
    response = ask_gemini(prompt, parameters, document)
    cleaned_response = clean_llm_response(response)

    try:
        response_json = json.loads(cleaned_response)
    except json.decoder.JSONDecodeError:
        try:
            cleaned_response = clean_quotes_from_json(cleaned_response)
            response_json = json.loads(cleaned_response)
        # for excel logic
        except json.JSONDecodeError:
            # Replace single quotes with double quotes
            cleaned_response = re.sub(r"(?<!\\)'", '"', cleaned_response)
            response_json = json.loads(cleaned_response)
    return response_json


def prompt_excel_extraction(excel_structured_text, schema):
    """Write a prompt to extract data from Excel files.

    Args:
        excel_structured_text (str): The structured text of the Excel file.
        schema (str): The schema of the data to extract

    Returns:
        prompt str: The prompt for common json.
    """
    footnote = "return the extracted data as a single output in a dictionary format {}."

    prompt = f"""{excel_structured_text}

    Task: Fill in the following dictionary from the information in the given in the above excel data.

    Instructions:
    - Do not change the keys of the following dictionary.
    - The values should be filled in as per the schema provided below.
    - If an entity contains a 'display_name', consider its properties as child data points in the below format.
    {{'data-field': {{
        'child-data-field': 'type -occurrence_type- description',
          }}
    }}
    - The entity with 'display_name' can be extracted multiple times. Please pay attention to the occurrence_type.
    - Ensure the schema reflects the hierarchical relationship.
    - Use the data field description to understand the context of the data.

    The schema is as follows:
    {schema}

    {footnote}
    """
    return prompt


def prepare_document_for_gemini(file_content):
    """Prepare a document from file content by encoding it to base64.

    Args:
        file_content (bytes): The binary content of the file to be processed.

    Returns:
        Part: A document object ready for processing by the language model.
    """
    # Convert binary file to base64
    pdf_base64 = base64.b64encode(file_content).decode('utf-8')
    
    # Create the document for the model
    document = Part.from_data(mime_type="application/pdf", data=base64.b64decode(pdf_base64))
    
    return document


def create_client_chatgpt():
    client = OpenAI(
        base_url="https://api.langdock.com/openai/eu/v1",
        api_key="sk-JxVOORbV8j2AVYmMuGeQc-arZxdnEJMl96ptSeqSZsOKbIBIDGLdd0vZUXwkY8avZR0puw09tlqD9Lx38cGaDA"
    )
    return client

def ask_chatgpt(prompt: str, chatgpt_client=None, document=None):
    """Ask the chatgpt model a question.

    Args:
        prompt (str): The prompt to ask the model.
        document (base64): the image to send the model
    Returns:
        str: The response from the model.
    """
    if chatgpt_client is None:
        chatgpt_client = create_client_chatgpt()

    if document is None:
        completion = chatgpt_client.chat.completions.create(
            model="gpt-4o",
            temperature=0.1,
            messages= [{
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    }
                ]
                }
            ]
        )
    else:
        completion = chatgpt_client.chat.completions.create(
            model="gpt-4o",
            temperature=0.1,
            messages= [{
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{document}",
                        },
                    },
                ]
                }
            ]
        )

    response = completion.choices[0].message.content
    return response

def get_unified_json_chatgpt(prompt, document=None):
    """Send a prompt to a Google Cloud AI Platform model and returns the generated json.

    Args:
        prompt (str): The prompt to send to the LLM model.
        parameters (dict, optional): The parameters to use for the model. Defaults to None.

    Returns:
        dict: The generated json from the model.
    """
    # Ask the LLM model
    response = ask_gemini(prompt, document)
    cleaned_response = clean_llm_response(response)

    try:
        response_json = json.loads(cleaned_response)
    except json.decoder.JSONDecodeError:
        try:
            cleaned_response = clean_quotes_from_json(cleaned_response)
            response_json = json.loads(cleaned_response)
        # for excel logic
        except json.JSONDecodeError:
            # Replace single quotes with double quotes
            cleaned_response = re.sub(r"(?<!\\)'", '"', cleaned_response)
            response_json = json.loads(cleaned_response)
    return response_json