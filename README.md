An e-commerce analytics organization aims to extract and utilize data from user purchase bills (provided in image format) for various analytical purposes.

Used langgraph react agent as the main chat agent (conversation_agent). It has access to two tools InvoiceExtractor and save_invoice_data.

How it works:
1. The user interacts with the agent by typing messages.
2. The conversation_agent receives the user's input and uses the conversation_agent_prompt and the LLM to determine the next action.
3. Based on the user's request, the agent might decide to use one of the available tools:
    - If the user provides an image URL (Assuming that the user has uploaded the image and we are directly receiving its url) or implicitly refers to an invoice, the agent might use the InvoiceExtractor tool to extract information from the image.
    - If the agent has extracted invoice data, it might use the save_invoice_data tool to save the information to a JSON file.
    - The InvoiceExtractor tool takes an image URL, reads the image (or uses a local default), converts it to Base64, and sends it along with a prompt (defined in invoice_extractor_prompt and incorporating the schema from predefined_schema.json) to the Groq LLM.
4. The Groq LLM processes the image and the prompt and returns the extracted information (likely as a JSON string).
5. The save_invoice_data tool takes this extracted JSON string and saves it to a file.
6. The agent then responds to the user based on the outcome of the tool usage or its internal reasoning.


Model used: meta-llama/llama-4-scout-17b-16e-instruct 

A Sample Conversation: 
User: Hi 
Agent: Hello! I'm here to help you with your purchase invoices and bills. How can I assist you today? Do you have an invoice you'd like me to heth?

User: invoice_url = https://www.image_url.com (User upload the image to the system and we get the URL like this, for simplicity its     default right now/hardcoded)
System: The invoice details have been extracted successfully. Here's a summary:
* Invoice Number: IN-761
* Invoice Date: 28th October 2019
* Store Name: Varasiddhi Silk Exports
* Store Address: 75, 3rd Cross, Lalbagh Road, Bengaluru, Karnataka 560027
* Customer Name: Madhu B
* Customer Address: Eurofins IT Solutions India Pvt Ltd., 1st Floor, Maruti Platinum, Lakshminarayana Pura, AECS Layout, Bengaluru, Karnataka 56
* Item:["Varasiddhi Silks Men's Formal Shirt (SH-05-42, Navy Blue,42) B07KGF3KW8 ( SH-05--42 )","Varasiddhi Silks Men's Formal Shirt (SH-05-40, Navy Blue,42) B07KGCX2S7 ( SH-05--40 )"]
* Quantity: 1
* Unit Price: ["₹538.10","₹538.10"]
* Item Total Price: ₹1195.00
* Tax / GST / VAT Amount: ₹56.88

Would you like to know anything specific about this invoice or would you like to save/export the data?

User: What was the total bill amount? 
Agent: The total bill amount is ₹1195.00 (Item Total Price) + ₹56.88 (Tax / GST / VAT Amount) = ₹578.45.

User: Tell me about the items.
Agent: * Item Name/Description: Varasiddhi Silks Men's Formal Shirt (SH-05-42, Navy Blue,42) B07KGF3KW8 ( SH-05--42 )
* Quantity: 1
* Unit Price: 538.10
* Item Total Price: 565.00

* Item Name/Description: Varasiddhi Silks Men's Formal Shirt (SH-05-40, Navy Blue,42) B07KGCX2S7 ( SH-05--40)
* Quantity: 1
* Unit Price: 538.10
* Item Total Price: 565.00

Let me know if you'd like to know more about the invoice or perform any other actions!

User: I want to export the data. 
Agent: The invoice data has been successfully exported as a JSON file.Let me know if you need any further assistance!
