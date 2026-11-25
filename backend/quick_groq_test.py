import asyncio
from app.database import settings
from app.services.groq_service import get_groq_service

async def test():
    print("Testing Groq API...")
    print(f"API Key: {settings.groq_api_key[:20]}...")
    print(f"Model: {settings.groq_model}")
    print()
    
    service = get_groq_service()
    print("Calling Groq API...")
    
    try:
        result = await service.analyze_text(
            prompt="Say 'Hello from Groq!' if you can read this.",
            system_prompt="You are a helpful assistant. Be concise.",
            temperature=0.1
        )
        
        print("SUCCESS! Groq API is working!")
        print(f"Response: {result}")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test())
    exit(0 if success else 1)
