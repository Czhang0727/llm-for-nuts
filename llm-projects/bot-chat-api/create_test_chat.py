#!/usr/bin/env python3
"""
Script to create a test chat session with random messages
"""
import uuid
import random
from database import DatabaseManager
from datetime import datetime

# Sample messages for testing
SAMPLE_MESSAGES = [
    "Hello! How are you today?",
    "I'm doing great, thank you for asking!",
    "What's the weather like where you are?",
    "It's sunny and warm here, perfect for a walk.",
    "That sounds lovely! I wish I could go outside.",
    "You should definitely take a break and enjoy the sunshine!",
    "Thanks for the encouragement. I'll try to get some fresh air later.",
    "That's a great idea. Fresh air always helps clear the mind.",
    "What are your plans for the weekend?",
    "I'm planning to visit a local park and maybe read a book.",
    "That sounds relaxing. What book are you reading?",
    "I'm currently reading a science fiction novel about space exploration.",
    "That sounds interesting! I love science fiction stories.",
    "Me too! They always spark my imagination.",
    "Do you have any recommendations for good sci-fi books?",
    "I'd recommend 'The Three-Body Problem' or 'Dune' - both are excellent!",
    "Thanks for the suggestions! I'll check them out.",
    "You're welcome! I hope you enjoy them as much as I did.",
    "I'm sure I will. Thanks for the chat!",
    "It was great talking with you too. Have a wonderful day!"
]


def create_test_chat(num_messages: int = 10) -> str:
    """
    Create a test chat session with random messages
    
    Args:
        num_messages: Number of messages to create (default: 10)
        
    Returns:
        Session ID of the created chat
    """
    db_manager = DatabaseManager()
    
    # Create a new session
    session_id = str(uuid.uuid4())
    title = f"Test Chat - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    print(f"📝 Creating test chat session...")
    print(f"   Session ID: {session_id}")
    print(f"   Title: {title}")
    
    try:
        # Create session in database
        db_manager.create_session(session_id, title)
        print(f"✅ Session created successfully")
        
        # Add random messages
        print(f"\n💬 Adding {num_messages} messages...")
        selected_messages = random.sample(SAMPLE_MESSAGES, min(num_messages, len(SAMPLE_MESSAGES)))
        
        for i, message_content in enumerate(selected_messages, 1):
            message_id = db_manager.add_message(session_id, message_content)
            print(f"   [{i}] Message ID {message_id}: {message_content[:50]}...")
        
        print(f"\n✅ Test chat created successfully!")
        print(f"\n📊 Summary:")
        print(f"   Session ID: {session_id}")
        print(f"   Title: {title}")
        print(f"   Messages: {len(selected_messages)}")
        
        # Verify messages
        messages = db_manager.get_messages(session_id)
        print(f"\n✅ Verified: {len(messages)} messages in database")
        
        return session_id
        
    except Exception as e:
        print(f"❌ Error creating test chat: {str(e)}")
        raise


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Create a test chat session with random messages"
    )
    parser.add_argument(
        '--messages',
        type=int,
        default=10,
        help='Number of messages to create (default: 10)'
    )
    
    args = parser.parse_args()
    
    try:
        session_id = create_test_chat(args.messages)
        print(f"\n🔗 To retrieve messages, use:")
        print(f"   GET /api/chat/{session_id}/messages")
        print(f"\n   Or test with curl:")
        print(f"   curl http://localhost:5000/api/chat/{session_id}/messages")
    except Exception as e:
        print(f"\n❌ Failed to create test chat: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()

