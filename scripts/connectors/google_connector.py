#!/usr/bin/env python3
"""
Google Gemini LLM Connector

This module handles connections to Google's Gemini API.
NOTE: This connector needs to be updated and tested as it may not be working correctly.
"""

import os
import time
import logging
from typing import Tuple, Optional

from google.generativeai import GenerativeModel, configure
import google.generativeai as genai

from .base_connector import BaseLLMConnector

logger = logging.getLogger("ai_ethics")

class GoogleConnector(BaseLLMConnector):
    """Google Gemini API connector - NEEDS UPDATING"""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None, base_path: Optional[str] = None, instructions: Optional[str] = None):
        """
        Initialize Google Gemini connector

        Args:
            api_key: Google API key (if None, will look for GEMINI_API_KEY env var)
            model_name: Model name (if None, will use GEMINI_MODEL env var or default)
            base_path: Base path to the project root
            instructions: Custom instructions for the model (if None, uses default)
        """
        if api_key is None:
            api_key = os.environ.get("GEMINI_API_KEY")

        if model_name is None:
            model_name = os.environ.get("GEMINI_MODEL", "gemini-1.5-pro")

        super().__init__(api_key, model_name, base_path)

        # Set instructions - use provided or default
        self.instructions = instructions or "You are an expert grant reviewer for the School of Health Professions Research Seed Grant program."

        if self.api_key:
            self._initialize_client()
        else:
            logger.warning("Google Gemini API key not found. Gemini functionality will be disabled.")

    def _initialize_client(self) -> bool:
        """
        Initialize the Google Gemini client

        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            configure(api_key=self.api_key)
            self.client = GenerativeModel(self.model_name)
            self.is_initialized = True
            logger.info(f"Google Gemini client initialized with model {self.model_name}")
            return True
        except Exception as e:
            logger.error(f"Error initializing Google Gemini client: {e}")
            self.is_initialized = False
            return False

    def query(self, prompt: str) -> Tuple[str, float, str, str, str]:
        """
        Query the Google Gemini API with the given prompt

        NOTE: This method needs to be updated and tested as it may not work correctly.

        Args:
            prompt: The prompt to send to Google Gemini

        Returns:
            Tuple containing:
            - response_text: The response from Google Gemini
            - processing_time: Time taken to process the request
            - model_name: Name of the model used
            - model_version: Version of the model used
            - actual_prompt: The actual full prompt sent to the API

        Raises:
            ValueError: If the client is not initialized
            Exception: If there's an error querying the Google Gemini API
        """
        if not self.client:
            raise ValueError("Google Gemini client not initialized")

        start_time = time.time()
        try:
            # Combine instructions with prompt for Gemini (it doesn't have separate system messages)
            full_prompt = f"{self.instructions}\n\n{prompt}"
            response = self.client.generate_content(full_prompt)
            processing_time = time.time() - start_time

            # Get model version if available, otherwise use the model name
            try:
                model_version = response.candidates[0].safety_ratings[0].model_version if hasattr(response, 'candidates') else self.model_name
            except (AttributeError, IndexError):
                model_version = self.model_name

            return response.text, processing_time, self.model_name, model_version, full_prompt
        except Exception as e:
            logger.error(f"Error querying Google Gemini: {e}")
            raise

    def get_vendor_name(self) -> str:
        """Get the vendor name for Google"""
        return "Google"