#!/usr/bin/env python3
"""
Video Generation Demo
Takes a prompt from console.
"""

from openai import OpenAI
import os


def generate_video(prompt: str) -> str:
    """Generate a video based on a prompt."""
    # Initialize OpenAI client (reads API key from OPENAI_API_KEY env var)
    client = OpenAI()
    response = client.videos.create(
        model="sora-2",
        prompt=prompt
    )
    print(response)

import requests, os

def generate_video_with_sora(prompt):
    endpoint = "https://api.openai.com/v1/"
    headers = {
        "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "sora-2",
        "prompt": prompt,
    }
    response = requests.post(f"{endpoint}/videos",
                             headers=headers, json=body)
    
    print(response.json())
    return response.json()

def list_models():
    openai_client = OpenAI()
    models = openai_client.models.list()
    print("Available models:")
    for model in models.data:
        print(f"  - {model.id}")
    return models


def main():
    """Main function to run the video generator."""
    # Get prompt from console
    list_models()
    
    prompt = input("Enter your video prompt: ").strip()
    
    if not prompt:
        print("Error: Prompt cannot be empty!")
        return 1
    
    generate_video_with_sora(prompt)
    
    print(f"Prompt received: '{prompt}'")
    
    return 0


if __name__ == "__main__":
    exit(main())
