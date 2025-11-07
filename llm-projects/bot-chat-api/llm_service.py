"""
LLM service for interacting with OpenAI and Dashscope APIs
"""
from typing import List, Dict, Literal
from config import settings
import openai
import dashscope


class LLMService:
    """Service for interacting with LLM providers"""
    
    def __init__(self):
        """Initialize LLM service with configured provider"""
        self.provider = settings.LLM_PROVIDER
        
        if self.provider == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is required for OpenAI provider")
            openai.api_key = settings.OPENAI_API_KEY
            self.model = settings.OPENAI_MODEL
        elif self.provider == "dashscope":
            if not settings.DASHSCOPE_API_KEY:
                raise ValueError("DASHSCOPE_API_KEY is required for Dashscope provider")
            dashscope.api_key = settings.DASHSCOPE_API_KEY
            self.model = settings.DASHSCOPE_MODEL
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    async def get_completion(
        self,
        messages: List[Dict[str, str]]
    ) -> str:
        """
        Get completion from LLM provider
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys
            
        Returns:
            Generated response text
        """
        if self.provider == "openai":
            return await self._get_openai_completion(messages)
        elif self.provider == "dashscope":
            return await self._get_dashscope_completion(messages)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    async def _get_openai_completion(
        self,
        messages: List[Dict[str, str]]
    ) -> str:
        """Get completion from OpenAI"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def _get_dashscope_completion(
        self,
        messages: List[Dict[str, str]]
    ) -> str:
        """Get completion from Dashscope"""
        try:
            response = dashscope.Generation.call(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            if response.status_code == 200:
                return response.output.choices[0].message.content
            else:
                raise Exception(f"Dashscope API error: {response.message}")
        except Exception as e:
            raise Exception(f"Dashscope API error: {str(e)}")

