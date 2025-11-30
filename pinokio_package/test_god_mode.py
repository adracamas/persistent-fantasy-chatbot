#!/usr/bin/env python3
"""
Test the database fix and god-like control features.
"""

import tempfile
import os

def test_database_fix():
    """Test that the database fix works correctly."""
    print("🔧 Testing Database Fix...")
    print("-" * 40)
    
    from memory_system import FantasyMemorySystem
    
    # Use temporary database file
    temp_db = tempfile.mktemp(suffix='.db')
    try:
        memory = FantasyMemorySystem(temp_db)
        print("✅ Memory system initialized")
        
        # Test storing memory
        memory_id = memory.store_memory(
            "Thorin Ironbeard is a friendly dwarf bartender",
            "character",
            "Thorin",
            {"race": "dwarf", "role": "barkeeper"},
            importance=8
        )
        print("✅ Memory stored successfully")
        
        # Test retrieval
        results = memory.retrieve_relevant_memories("Tell me about the dwarf", limit=3)
        print(f"✅ Retrieved {len(results)} memories")
        
        if results:
            print(f"   Top result: {results[0]['name']} - {results[0]['content']}")
        
        # Test auto-extraction
        extracted = memory.auto_extract_memories(
            "I meet Eldara the Elf Queen in her crystal palace",
            "Eldara welcomes you to her magnificent palace"
        )
        print(f"✅ Auto-extracted {len(extracted)} memories")
        
        print("✅ Database fix working correctly!\n")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists(temp_db):
            os.unlink(temp_db)

def test_god_like_control():
    """Test the god-like control system."""
    print("👑 Testing God-Like Control...")
    print("-" * 40)
    
    try:
        from local_llm import LocalFantasyLLM
        
        # Test prompt creation
        llm = LocalFantasyLLM()
        
        # Create a test prompt
        test_memories = [{
            'name': 'Thorin',
            'content': 'A friendly dwarf bartender at The Prancing Pony',
            'type': 'character'
        }]
        
        test_world_state = [{
            'state_type': 'location',
            'key': 'current_location',
            'value': 'The Prancing Pony tavern'
        }]
        
        prompt = llm.create_fantasy_prompt(
            user_input="I enter the tavern",
            relevant_memories=test_memories,
            world_state=test_world_state,
            conversation_history=[]
        )
        
        print("✅ Prompt created with god-like control system")
        
        # Check that the prompt contains the authority directives
        if "You ARE the world itself" in prompt:
            print("✅ God-like authority prompt found")
        else:
            print("❌ God-like authority prompt missing")
            return False
            
        if "god mode" in prompt.lower():
            print("✅ God mode keywords present")
        else:
            print("❌ God mode keywords missing")
            return False
        
        if "NEVER ask" in prompt:
            print("✅ Anti-question directives present")
        else:
            print("❌ Anti-question directives missing")
            return False
            
        print("✅ God-like control system working correctly!\n")
        return True
        
    except Exception as e:
        print(f"❌ God-like control test failed: {e}")
        return False

def test_integration():
    """Test the full integration of both systems."""
    print("🎯 Testing Full Integration...")
    print("-" * 40)
    
    try:
        # Import both systems
        from memory_system import FantasyMemorySystem
        from local_llm import LocalFantasyLLM
        from fantasy_chatbot import FantasyChatbot
        
        print("✅ All components imported successfully")
        
        # Test that the chatbot can initialize with fixed database
        chatbot = FantasyChatbot()
        print("✅ Chatbot initialized with fixed memory system")
        
        # Test memory stats
        stats = chatbot.get_memory_stats()
        print(f"✅ Memory stats accessible: {stats['total_memories']} memories")
        
        print("✅ Full integration test passed!\n")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 COMPREHENSIVE SYSTEM TESTS")
    print("=" * 50)
    print()
    
    # Run tests
    db_test = test_database_fix()
    god_test = test_god_like_control()
    int_test = test_integration()
    
    # Summary
    print("📊 Test Results Summary")
    print("-" * 50)
    print(f"Database Fix:     {'✅ PASS' if db_test else '❌ FAIL'}")
    print(f"God-Like Control: {'✅ PASS' if god_test else '❌ FAIL'}")
    print(f"Integration:      {'✅ PASS' if int_test else '❌ FAIL'}")
    
    if all([db_test, god_test, int_test]):
        print("\n🎉 ALL TESTS PASSED!")
        print("Your fantasy chatbot is ready for god-like adventures!")
        print("\nNext steps:")
        print("1. python setup.py")
        print("2. python fantasy_chatbot.py")
        print("3. Begin your persistent fantasy journey! 🏰")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")

if __name__ == "__main__":
    main()