#!/usr/bin/env python3
"""
Video Generation Demo
Takes a prompt from console.
"""


def main():
    """Main function to run the video generator."""
    # Get prompt from console
    prompt = input("Enter your video prompt: ").strip()
    
    if not prompt:
        print("Error: Prompt cannot be empty!")
        return 1
    
    print(f"Prompt received: '{prompt}'")
    
    return 0


if __name__ == "__main__":
    exit(main())
