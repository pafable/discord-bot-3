# pylint: disable=C0114,C0301,R0903

import enum
from typing import Final
import boto3


AWS_REGION: Final[str] = "us-east-1"

class BedrockCursor:
    """
    Create a cursor to send prompts to bedrock using a specific model and get output back from the model
    """
    def __init__(self, model_id: str):
        self.id = model_id

    def get_message(self, prompt) -> str:
        """
        Get message from bedrock
        """
        client = boto3.client(service_name="bedrock-runtime", region_name=AWS_REGION)

        inference_config = {
            "maxTokens": 4096
        }

        message = [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]

        resp = client.converse(
            inferenceConfig=inference_config,
            modelId=self.id,
            messages=message
        )

        return resp["output"]["message"]["content"][0]["text"]


class LLMmodel(enum.Enum):
    """
    Uses models found in below:
    https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html

    Have to use inference profiles for some models
    https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/inference-profiles
    """
    CLAUDE_3_5_SONNET = ("us.anthropic.claude-3-5-sonnet-20240620-v1:0", "Claude 3.5 Sonnet", "Anthropic")
    CLAUDE_3_5_SONNET_V2 = ("us.anthropic.claude-3-5-sonnet-20241022-v2:0", "Claude 3.5 Sonnet v2", "Anthropic")
    LLAMA_3_2_90B_INSTRUCT_V1 = ("us.meta.llama3-2-90b-instruct-v1:0", "Llama 3.2 90B Instruct", "Meta")
    TITAN_TEXT_LITE = ("amazon.titan-text-lite-v1", "Titan Text G1 - Lite", "Amazon")
    TITAN_TEXT_G1_EXPRESS = ("amazon.titan-text-express-v1", "Titan Text G1 - Express", "Amazon")

    def __init__(
            self,
            model_id: str,
            name: str,
            provider: str
    ) -> None:
        self.id =  model_id
        self.llm_name = name
        self.provider = provider
