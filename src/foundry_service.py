import os
import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential
from agent_framework import ChatMessage, TextContent, DataContent, Role
from utils import pdf_to_images

from dotenv import load_dotenv
load_dotenv(override=True)

agent = AzureOpenAIChatClient(
    credential=DefaultAzureCredential(),
    endpoint=os.getenv("AI_FOUNDRY_ENDPOINT"),
    api_key=os.getenv("AI_FOUNDRY_API_KEY"),
    deployment_name="gpt-4.1"
).create_agent(
    instructions="You're a document analyzer.",
    name="DocumentAnalyzer"
)


async def pre_process_pdf(pdf_file_path) -> list:
    # Convert PDF to images
    images = pdf_to_images(pdf_file_path)

    pre_process_result = []
    # Process each image
    for image in images:
        message = ChatMessage(
            role=Role.USER,
            contents=[
                TextContent(text="""
                            Analyze the following image and classify it if it's an invoice or not. 
                            Reply ONLY with 'Yes' if it is an invoice, 'No' otherwise.
                            Do not include any other text in your response."""),
                DataContent(
                    data=image["bytes"],
                    media_type="image/png"
                )
            ]
        )

        # Send message to agent and receive response
        response = await agent.run(messages=message)

        # Print usage details
        print(response.usage_details)

        # Process response
        result = True if response.text.lower().startswith("yes") else False
        print({f"Page {image['page_num']} is an invoice": result})

        # Append result to process_result list
        pre_process_result.append({
            "page_num": image["page_num"],
            "is_invoice": result
        })

    # Return the process result list
    return pre_process_result


if __name__ == "__main__":
    asyncio.run(pre_process_pdf("453-3633210941.pdf"))
    # byte_stream_images = pdf_to_images("453-2426288.pdf")
    # output = mistral_image_ocr(byte_stream_images[0])
    # output = mistral_pdf_ocr(open("453-3633210941.pdf", "rb").read())
    # print(output)
