#!/usr/bin/env python3
"""
Image Generation Demo
Takes a prompt from console and generates an image using Qwen's API.
"""

from dashscope import ImageSynthesis
import os


def main():
    """Main function to run the image generator."""
    # Get prompt from console
    prompt = input("Enter your image prompt: ").strip()
    
    if not prompt:
        print("Error: Prompt cannot be empty!")
        return 1
    
    # Check if API key is set
    api_key = os.getenv('DASHSCOPE_API_KEY')
    if not api_key:
        print("Error: DASHSCOPE_API_KEY environment variable is not set.")
        print("Please set it with: export DASHSCOPE_API_KEY='your-api-key'")
        return 1
    
    # Generate image using Qwen
    result = ImageSynthesis.call(
        model='wanx-v1',
        prompt=prompt,
        n=1,
        size='1024*1024'
    )
    
    # Print image URL
    if result.status_code == 200:
        image_url = result.output.results[0].url
        print(image_url)
        return 0
    else:
        print(f"Error: {result.status_code}, {result.message}")
        return 1


if __name__ == "__main__":
    exit(main())

