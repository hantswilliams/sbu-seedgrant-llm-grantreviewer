#!/usr/bin/env python3
"""
Base LLM Connector

This module defines the base class that all LLM connectors should inherit from.
"""

import os
import time
import logging
from abc import ABC, abstractmethod
from typing import Tuple, Optional
from pathlib import Path

logger = logging.getLogger("ai_ethics")

class BaseLLMConnector(ABC):
    """Base class for all LLM connectors"""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None, base_path: Optional[Path] = None, instructions: Optional[str] = None):
        """
        Initialize the connector

        Args:
            api_key: API key for the service
            model_name: Model name to use
            base_path: Base path to the project root
            instructions: Grant review instructions (if None, will load default)
        """
        self.api_key = api_key
        self.model_name = model_name
        self.client = None
        self.is_initialized = False

        # Set base path for loading instructions
        if base_path is None:
            self.base_path = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        else:
            self.base_path = Path(base_path)

        # Use provided instructions or load default
        if instructions:
            self.grant_review_instructions = instructions
            logger.info("Using provided grant review instructions")
        else:
            self.grant_review_instructions = self._load_grant_review_instructions()

    @abstractmethod
    def _initialize_client(self) -> bool:
        """
        Initialize the API client

        Returns:
            bool: True if initialization successful, False otherwise
        """
        pass

    @abstractmethod
    def query(self, prompt: str) -> Tuple[str, float, str, str, str]:
        """
        Query the LLM with the given prompt

        Args:
            prompt: The prompt to send to the LLM

        Returns:
            Tuple containing:
            - response_text: The response from the LLM
            - processing_time: Time taken to process the request
            - model_name: Name of the model used
            - model_version: Version of the model used
            - actual_prompt: The actual full prompt sent to the API

        Raises:
            ValueError: If the client is not initialized
            Exception: If there's an error querying the API
        """
        pass

    def is_available(self) -> bool:
        """
        Check if this connector is available (initialized and ready to use)

        Returns:
            bool: True if available, False otherwise
        """
        return self.is_initialized and self.client is not None

    def get_vendor_name(self) -> str:
        """
        Get the vendor name for this connector

        Returns:
            str: Vendor name
        """
        return self.__class__.__name__.replace('Connector', '')

    def _load_grant_review_instructions(self) -> str:
        """
        Load the grant review instructions from the llm/prompts directory
        Defaults to baseline_v1.md if no instructions provided

        Returns:
            str: The grant review instructions
        """
        instructions_path = self.base_path / "llm" / "prompts" / "baseline_v1.md"
        try:
            with open(instructions_path, 'r') as f:
                instructions = f.read()
                logger.info(f"Loaded default grant review instructions from {instructions_path}")
                return instructions
        except Exception as e:
            logger.error(f"Error loading grant review instructions from {instructions_path}: {e}")
            # Return default instructions if file not found
            return "You are an expert grant reviewer for the School of Health Professions Research Seed Grant program."