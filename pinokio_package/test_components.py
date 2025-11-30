#!/usr/bin/env python3
"""
Quick test to verify Fantasy Chatbot components work
"""

def test_memory_system():
    """Test the memory system without LLM."""
    print("🧪 Testing Memory System...")
    
    try:
        from memory_system import FantasyMemorySystem
        
        # Create in-memory database for testing
        memory = FantasyMemorySystem(":memory:")
        
        # Test storing memories
        memory_id = memory.store_memory(
            "Thorin is a friendly dwarf bartender",
            "character",
            "Thorin",
            {"race": "dwarf", "role": "barkeeper"},
            importance=8
        )
        
        # Test retrieval
        memories = memory.retrieve_relevant_memories("Tell me about Thorin", limit=3)
        
        assert len(memories) > 0, "Should find relevant memory"
        assert memories[0]['name'] == 'Thorin', "Should find Thorin memory"
        assert memories[0]['type'] == 'character', "Should be character type"
        
        # Test conversation storage
        memory.store_conversation("test_session", "Hello", "Hi there!")
        history = memory.get_conversation_history("test_session")
        assert len(history) > 0, "Should store conversation"
        
        # Test world state
        memory.set_world_state("time", "morning", "It's early morning")
        world_state = memory.get_world_state("time")
        assert len(world_state) > 0, "Should store world state"
        
        print("✅ Memory System: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Memory System: FAILED - {e}")
        return False

def test_embeddings():
    """Test embedding generation."""
    print("🧪 Testing Embeddings...")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        # Load small model for testing
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Test embedding generation
        embeddings = model.encode([
            "The dwarf bartender Thorin",
            "A friendly tavern keeper", 
            "Completely unrelated text"
        ])
        
        assert embeddings.shape[0] == 3, "Should encode 3 texts"
        assert embeddings.shape[1] == 384, "Should be 384 dimensions"
        
        # Test similarity calculation
        from sklearn.metrics.pairwise import cosine_similarity
        
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        assert similarity > 0.5, "Similar texts should have high similarity"
        
        similarity = cosine_similarity([embeddings[0]], [embeddings[2]])[0][0] 
        assert similarity < 0.5, "Different texts should have low similarity"
        
        print("✅ Embeddings: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Embeddings: FAILED - {e}")
        return False

def test_web_interface():
    """Test web interface imports."""
    print("🧪 Testing Web Interface...")
    
    try:
        import fastapi
        import uvicorn
        import websockets
        
        print("✅ Web Interface: PASSED (imports successful)")
        return True
        
    except Exception as e:
        print(f"❌ Web Interface: FAILED - {e}")
        return False

def test_chatbot_components():
    """Test core chatbot components."""
    print("🧪 Testing Chatbot Components...")
    
    try:
        # Test imports
        from fantasy_chatbot import FantasyChatbot
        
        # Test initialization without LLM loading
        chatbot = FantasyChatbot()
        
        assert chatbot.session_id is not None, "Should have session ID"
        assert chatbot.memory_system is not None, "Should have memory system"
        
        print("✅ Chatbot Components: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Chatbot Components: FAILED - {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Fantasy Chatbot Component Tests")
    print("=" * 40)
    
    tests = [
        test_memory_system,
        test_embeddings,
        test_web_interface,
        test_chatbot_components
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests Passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All tests passed! Ready to launch.")
    else:
        print("⚠️  Some tests failed. Check error messages above.")
    
    return passed == len(tests)

if __name__ == "__main__":
    main()