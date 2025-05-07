from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv 
from langchain_groq import ChatGroq
import json
from langgraph.prebuilt import create_react_agent
import base64
import os
from prompt import invoice_extractor_prompt,conversation_agent_prompt
from langgraph.checkpoint.memory import MemorySaver
import json 

load_dotenv()

DEFAULT_URL = "https://www.image_url.com"

# Initialize Groq LLM
llm = ChatGroq(
    model_name="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0
)


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

#Function for converting the image to base64 for sending the image to the LLM 
def image_to_base64(image_path: str) -> str:
    """
    Converts an image file to its Base64 string representation.

    Args:
        image_path: The path to the image file.

    Returns:
        A string containing the Base64 encoded image data, or None if
        the file is not found or an error occurs.
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    except FileNotFoundError:
        print(f"Error: Image file not found at '{image_path}'")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

#Tool for exporting the invoice data to JSON
def save_invoice_data(json_output, output_path='invoice_output.json'):
    """
    Parses the extracted JSON string from the invoice extractor
    and saves it as a formatted JSON file.

    Parameters:
    - json_output (str or dict): JSON string or dict from the extractor
    - output_path (str): File path to save the JSON (default: 'invoice_output.json')

    Returns:
    - str: The absolute path of the saved JSON file
    """
    try:
        if isinstance(json_output, str):
            data = json.loads(json_output)
        elif isinstance(json_output, dict):
            data = json_output
        else:
            raise ValueError("Input must be a JSON string or Python dict.")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        abs_path = os.path.abspath(output_path)
        print(f"Invoice data saved successfully at: {abs_path}")
        return abs_path

    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
    except Exception as e:
        print(f"Error saving invoice data: {e}")

# Tool for extracting the invoice data based on the 
def InvoiceExtractor(image_url: str):
    """
    Extracts information from an invoice image using a language model.

    Args:
        image_url: The URL of the invoice image to process. 

    Returns:
        str: The extracted information from the invoice as a string.
    """
    with open('./predefined_schema.json', 'r') as file:
        predefined_schema = json.load(file)
    required_feilds = str(list(predefined_schema.keys()))
    message = [{
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": invoice_extractor_prompt.replace("$required_fields",str(list(required_feilds))),
            },
        ],
    }]
    if image_url == DEFAULT_URL:
        image_data = image_to_base64("./invoices/invoice2.png")
        message[0]["content"].append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_data}",
                }
            }
        )

    else:
        message[0]["content"].append(
            {

                "type": "image_url",
                "image_url": {
                    "url": image_url
                }
            }
        )

    response = llm.invoke(message).content
    print(type(response), response)
    # save_invoice_data(response)
    return response



memory = MemorySaver()

#Our Main Agent 
conversation_agent = create_react_agent(
    model=llm,
    tools=[InvoiceExtractor,save_invoice_data],
    prompt=conversation_agent_prompt,
    name="conversation_agent",
    checkpointer= memory
)
config = {"configurable": {"thread_id": "1"}}

while True:
    user_input = input("User: ")
    if user_input.lower() == "quit":
        print("Exiting conversation.")
        break
    response = conversation_agent.invoke({"messages": [{"role": "user", "content": user_input}]}, config)
    print("Agent:", response["messages"][-1].content)


    
