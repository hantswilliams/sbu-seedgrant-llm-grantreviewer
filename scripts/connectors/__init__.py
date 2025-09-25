#!/usr/bin/env python3
"""
LLM Connectors Package

This package contains modular connectors for different LLM providers.
Each connector inherits from the BaseLLMConnector class and provides
a standardized interface for querying different AI models.

Available connectors:
- OpenAIConnector: Working connector for OpenAI's API using Responses API
- GoogleConnector: Google Gemini connector (needs updating)

Usage:
    from connectors import OpenAIConnector, GoogleConnector

    openai_conn = OpenAIConnector()
    if openai_conn.is_available():
        response, time, model, version = openai_conn.query("Your prompt here")
"""

from .base_connector import BaseLLMConnector
from .openai_connector import OpenAIConnector
from .google_connector import GoogleConnector

__all__ = [
    'BaseLLMConnector',
    'OpenAIConnector',
    'GoogleConnector'
]