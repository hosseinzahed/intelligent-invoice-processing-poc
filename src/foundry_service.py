import os
import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential
from agent_framework import ChatMessage, TextContent, DataContent, Role
from utils import pdf_to_images

# from dotenv import load_dotenv
# load_dotenv(override=True)

class FoundryService:

    def __init__(self):
        self.agent = AzureOpenAIChatClient(
            credential=DefaultAzureCredential(),
            endpoint=os.getenv("AI_FOUNDRY_ENDPOINT"),
            #api_key=os.getenv("AI_FOUNDRY_API_KEY"), # The API key is not needed when using DefaultAzureCredential
            deployment_name="gpt-4.1"
        ).create_agent(
            instructions="You're a document analyzer.",
            name="DocumentAnalyzer"
        )

    def pre_process_pdf(self, pdf_file_path: str) -> list:
        """Pre-process a PDF file to determine if each page is an invoice.
        Args:
            pdf_file_path (str): The path to the PDF file.
            Returns:
            list: A list of dictionaries containing page number, invoice status, image in base64, and token usage.
        """
        
        # Convert PDF to images
        images = pdf_to_images(pdf_file_path)

        pre_process_result = []
        # Process each image
        for image in images:
            message = ChatMessage(
                role=Role.USER,
                contents=[
                    TextContent(text="""
                                Analyze the attached image and classify it if it's an invoice or not. 
                                Reply ONLY with 'Yes' if it is an invoice, 'No' otherwise.
                                Do not include any other text in your response."""),
                    DataContent(
                        data=image["bytes"],
                        media_type="image/png"
                    )
                ]
            )

            # Send message to agent and receive response
            response = asyncio.run(self.agent.run(messages=message))

            # Process response
            result = True if response.text.lower().startswith("yes") else False

            # Append result to process_result list
            pre_process_result.append({
                "page_num": image["page_num"],
                "is_invoice": result,
                "image": image["base64"],
                "input_tokens": response.usage_details.input_token_count,
                "output_tokens": response.usage_details.output_token_count
            })

        # Return the process result list
        return pre_process_result


if __name__ == "__main__":
    pass
    # FoundryService().pre_process_pdf("435-2086_Invoice_Repeated_in_2pages.pdf")
    # byte_stream_images = pdf_to_images("453-2426288.pdf")
