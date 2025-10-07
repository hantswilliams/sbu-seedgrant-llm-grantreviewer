#!/usr/bin/env python3
"""
Anthropic LLM Connector

This module handles connections to Anthropic's Claude API.
"""

import os
import time
import logging
from typing import Tuple, Optional

import anthropic

from .base_connector import BaseLLMConnector

logger = logging.getLogger("ai_ethics")

class AnthropicConnector(BaseLLMConnector):
    """Anthropic Claude API connector"""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None, base_path: Optional[str] = None, instructions: Optional[str] = None):
        """
        Initialize Anthropic connector

        Args:
            api_key: Anthropic API key (if None, will look for ANTHROPIC_API_KEY env var)
            model_name: Model name (if None, will use ANTHROPIC_MODEL env var or default)
            base_path: Base path to the project root
            instructions: Custom instructions for the model (if None, uses default)
        """
        if api_key is None:
            api_key = os.environ.get("ANTHROPIC_API_KEY")

        if model_name is None:
            model_name = os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")

        # Pass instructions to parent class
        super().__init__(api_key, model_name, base_path, instructions)

        if self.api_key:
            self._initialize_client()
        else:
            logger.warning("Anthropic API key not found. Anthropic functionality will be disabled.")

    def _initialize_client(self) -> bool:
        """
        Initialize the Anthropic client

        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.is_initialized = True
            logger.info(f"Anthropic client initialized with model {self.model_name}")
            return True
        except Exception as e:
            logger.error(f"Error initializing Anthropic client: {e}")
            self.is_initialized = False
            return False

    def query(self, prompt: str) -> Tuple[str, float, str, str, str]:
        """
        Query the Anthropic API with the given prompt

        Args:
            prompt: The prompt to send to Claude

        Returns:
            Tuple containing:
            - response_text: The response from Claude
            - processing_time: Time taken to process the request
            - model_name: Name of the model used
            - model_version: Version of the model used
            - actual_prompt: The actual full prompt sent to the API

        Raises:
            ValueError: If the client is not initialized
            Exception: If there's an error querying the Anthropic API
        """
        if not self.client:
            raise ValueError("Anthropic client not initialized")

        start_time = time.time()
        try:
            # Build the full prompt with instructions
            full_prompt = f"{self.grant_review_instructions}\n\n{prompt}"

            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=4000,  # Ensure enough tokens for detailed reviews
                temperature=0.1,  # Keep responses consistent for evaluation
                messages=[
                    {"role": "user", "content": full_prompt}
                ]
            )
            processing_time = time.time() - start_time

            # Extract response text
            response_text = response.content[0].text

            # Extract model version from response if available
            model_version = getattr(response, 'model', self.model_name)

            return response_text, processing_time, self.model_name, model_version, full_prompt
        except Exception as e:
            logger.error(f"Error querying Anthropic: {e}")
            raise

    def get_vendor_name(self) -> str:
        """Get the vendor name for Anthropic"""
        return "Anthropic"