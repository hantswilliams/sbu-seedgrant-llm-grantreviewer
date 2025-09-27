#!/usr/bin/env python3
"""
Grok LLM Connector

This module handles connections to xAI's Grok API.
"""

import os
import time
import logging
from typing import Tuple, Optional

import openai

from .base_connector import BaseLLMConnector

logger = logging.getLogger("ai_ethics")

class GrokConnector(BaseLLMConnector):
    """Grok API connector using OpenAI-compatible API"""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None, base_path: Optional[str] = None, instructions: Optional[str] = None):
        """
        Initialize Grok connector

        Args:
            api_key: Grok API key (if None, will look for GROK_API_KEY env var)
            model_name: Model name (if None, will use GROK_MODEL env var or default)
            base_path: Base path to the project root
            instructions: Custom instructions for the model (if None, uses default)
        """
        if api_key is None:
            api_key = os.environ.get("GROK_API_KEY")

        if model_name is None:
            model_name = os.environ.get("GROK_MODEL", "grok-beta")

        super().__init__(api_key, model_name, base_path)

        # Set instructions - use provided or default
        self.instructions = instructions or "You are an expert grant reviewer for the School of Health Professions Research Seed Grant program."

        if self.api_key:
            self._initialize_client()
        else:
            logger.warning("Grok API key not found. Grok functionality will be disabled.")

    def _initialize_client(self) -> bool:
        """
        Initialize the Grok client

        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Grok uses OpenAI-compatible API with a different base URL
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url="https://api.x.ai/v1"
            )
            self.is_initialized = True
            logger.info(f"Grok client initialized with model {self.model_name}")
            return True
        except Exception as e:
            logger.error(f"Error initializing Grok client: {e}")
            self.is_initialized = False
            return False

    def query(self, prompt: str) -> Tuple[str, float, str, str, str]:
        """
        Query the Grok API with the given prompt

        Args:
            prompt: The prompt to send to Grok

        Returns:
            Tuple containing:
            - response_text: The response from Grok
            - processing_time: Time taken to process the request
            - model_name: Name of the model used
            - model_version: Version of the model used
            - actual_prompt: The actual full prompt sent to the API

        Raises:
            ValueError: If the client is not initialized
            Exception: If there's an error querying the Grok API
        """
        if not self.client:
            raise ValueError("Grok client not initialized")

        start_time = time.time()
        try:
            # Build messages for chat completion
            messages = [
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": prompt}
            ]

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.1,  # Keep responses consistent for evaluation
                max_tokens=4000   # Ensure enough tokens for detailed reviews
            )
            processing_time = time.time() - start_time

            # Extract response text
            response_text = response.choices[0].message.content

            # Extract model version from response if available
            model_version = getattr(response, 'model', self.model_name)

            # For consistency with other connectors, return the full prompt that represents what was sent
            full_prompt = f"{self.instructions}\n\n{prompt}"

            return response_text, processing_time, self.model_name, model_version, full_prompt
        except Exception as e:
            logger.error(f"Error querying Grok: {e}")
            raise

    def get_vendor_name(self) -> str:
        """Get the vendor name for Grok"""
        return "xAI"