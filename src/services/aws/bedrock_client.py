"""
AWS Bedrock client for LLM (alternative to OpenAI)
"""
import json
import logging

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class BedrockClient:
    """Client for AWS Bedrock LLM services"""

    def __init__(self):
        """Initialize Bedrock client"""
        # Use us-east-1 for Bedrock (better model availability)
        # Even though app is in ap-south-1, Bedrock calls can use different region
        bedrock_region = "us-east-1"

        self.client = boto3.client(
            'bedrock-runtime',
            region_name=bedrock_region
        )
        # Use Amazon Nova Lite - Better rate limits and cheaper than Llama
        self.model_id = "amazon.nova-lite-v1:0"
        self.model_type = "nova"  # Track which model we're using
        logger.info(f"Bedrock client initialized with model: {self.model_id} in region: {bedrock_region}")

    async def generate_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Generate completion using Bedrock

        Args:
            messages: List of message dicts with role and content
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text
        """
        try:
            if self.model_type == "llama":
                # Meta Llama format
                prompt = self._messages_to_simple_prompt(messages)

                body = json.dumps({
                    "prompt": prompt,
                    "max_gen_len": max_tokens,
                    "temperature": temperature,
                    "top_p": 0.9,
                })

                response = self.client.invoke_model(
                    modelId=self.model_id,
                    body=body
                )

                response_body = json.loads(response['body'].read())
                completion = response_body['generation']

            elif self.model_type == "nova":
                # Amazon Nova format (similar to OpenAI)
                body = json.dumps({
                    "messages": messages,
                    "inferenceConfig": {
                        "max_new_tokens": max_tokens,
                        "temperature": temperature,
                        "top_p": 0.9,
                    }
                })

                response = self.client.invoke_model(
                    modelId=self.model_id,
                    body=body,
                    contentType='application/json',
                    accept='application/json'
                )

                response_body = json.loads(response['body'].read())
                completion = response_body['output']['message']['content'][0]['text']

            elif self.model_type == "titan":
                # Amazon Titan format
                prompt = self._messages_to_simple_prompt(messages)

                body = json.dumps({
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": max_tokens,
                        "temperature": temperature,
                        "topP": 0.9,
                    }
                })

                response = self.client.invoke_model(
                    modelId=self.model_id,
                    body=body,
                    contentType='application/json',
                    accept='application/json'
                )

                response_body = json.loads(response['body'].read())
                completion = response_body['results'][0]['outputText']

            else:
                # Claude format (for future use)
                prompt = self._messages_to_prompt(messages)

                body = json.dumps({
                    "prompt": prompt,
                    "max_tokens_to_sample": max_tokens,
                    "temperature": temperature,
                    "top_p": 0.9,
                })

                response = self.client.invoke_model(
                    modelId=self.model_id,
                    body=body,
                    contentType='application/json',
                    accept='application/json'
                )

                response_body = json.loads(response['body'].read())
                completion = response_body.get('completion', '')

            logger.info(f"Generated {len(completion)} chars with Bedrock")
            return completion

        except ClientError as e:
            logger.error(f"Bedrock invocation failed: {e}")
            raise

    def _messages_to_prompt(self, messages: list[dict[str, str]]) -> str:
        """Convert OpenAI-style messages to Claude prompt format"""
        prompt_parts = []

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                prompt_parts.append(f"{content}\n")
            elif role == "user":
                prompt_parts.append(f"\n\nHuman: {content}")
            elif role == "assistant":
                prompt_parts.append(f"\n\nAssistant: {content}")

        # Add final Assistant prompt
        prompt_parts.append("\n\nAssistant:")

        return "".join(prompt_parts)

    def _messages_to_simple_prompt(self, messages: list[dict[str, str]]) -> str:
        """Convert OpenAI-style messages to simple prompt format (for Titan)"""
        prompt_parts = []

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                prompt_parts.append(f"Instructions: {content}\n\n")
            elif role == "user":
                prompt_parts.append(f"User: {content}\n\n")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}\n\n")

        prompt_parts.append("Assistant:")

        return "".join(prompt_parts)

    async def generate_embedding(self, text: str) -> list[float]:
        """
        Generate embeddings using Bedrock Titan

        Args:
            text: Input text

        Returns:
            Embedding vector
        """
        try:
            body = json.dumps({
                "inputText": text
            })

            response = self.client.invoke_model(
                modelId="amazon.titan-embed-text-v1",
                body=body,
                contentType='application/json',
                accept='application/json'
            )

            response_body = json.loads(response['body'].read())
            embedding = response_body.get('embedding', [])

            return embedding

        except ClientError as e:
            logger.error(f"Bedrock embedding failed: {e}")
            raise

    async def generate_text(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """
        Simple text generation (convenience method)

        Args:
            prompt: Text prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated text
        """
        messages = [{"role": "user", "content": prompt}]
        return await self.generate_completion(messages, temperature, max_tokens)
