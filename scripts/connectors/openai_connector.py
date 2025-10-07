#!/usr/bin/env python3
"""
OpenAI LLM Connector

This module handles connections to OpenAI's API using the Responses API.
"""

import os
import time
import logging
from typing import Tuple, Optional

import openai

from .base_connector import BaseLLMConnector

logger = logging.getLogger("ai_ethics")

class OpenAIConnector(BaseLLMConnector):
    """OpenAI API connector using the Responses API"""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None, base_path: Optional[str] = None, instructions: Optional[str] = None):
        """
        Initialize OpenAI connector

        Args:
            api_key: OpenAI API key (if None, will look for OPENAI_API_KEY env var)
            model_name: Model name (if None, will use OPENAI_MODEL env var or default)
            base_path: Base path to the project root
            instructions: Custom instructions for the model (if None, uses default)
        """
        if api_key is None:
            api_key = os.environ.get("OPENAI_API_KEY")

        if model_name is None:
            model_name = os.environ.get("OPENAI_MODEL", "gpt-4")

        # Pass instructions to parent class
        super().__init__(api_key, model_name, base_path, instructions)

        if self.api_key:
            self._initialize_client()
        else:
            logger.warning("OpenAI API key not found. OpenAI functionality will be disabled.")

    def _initialize_client(self) -> bool:
        """
        Initialize the OpenAI client

        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            self.client = openai.OpenAI(api_key=self.api_key)
            self.is_initialized = True
            logger.info(f"OpenAI client initialized with model {self.model_name}")
            return True
        except Exception as e:
            logger.error(f"Error initializing OpenAI client: {e}")
            self.is_initialized = False
            return False

    def query(self, prompt: str) -> Tuple[str, float, str, str, str]:
        """
        Query the OpenAI API with the given prompt using the Responses API

        Args:
            prompt: The prompt to send to OpenAI

        Returns:
            Tuple containing:
            - response_text: The response from OpenAI
            - processing_time: Time taken to process the request
            - model_name: Name of the model used
            - model_version: Version of the model used
            - actual_prompt: The actual full prompt (instructions + prompt for consistency)

        Raises:
            ValueError: If the client is not initialized
            Exception: If there's an error querying the OpenAI API
        """
        if not self.client:
            raise ValueError("OpenAI client not initialized")

        start_time = time.time()
        try:
            response = self.client.responses.create(
                model=self.model_name,
                instructions=self.grant_review_instructions,
                input=prompt
            )
            processing_time = time.time() - start_time

            # Extract model version from response if available
            model_version = getattr(response, 'model', self.model_name)

            # For consistency with Google connector, return the full prompt that represents what was sent
            full_prompt = f"{self.grant_review_instructions}\n\n{prompt}"

            return response.output_text, processing_time, self.model_name, model_version, full_prompt
        except Exception as e:
            logger.error(f"Error querying OpenAI: {e}")
            raise

    def get_vendor_name(self) -> str:
        """Get the vendor name for OpenAI"""
        return "OpenAI"