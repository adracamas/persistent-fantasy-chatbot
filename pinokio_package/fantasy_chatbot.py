"""
Persistent Fantasy Chatbot
Combines local LLM with memory system for immersive RPG experiences
"""

import os
import json
import uuid
import argparse
from datetime import datetime
from typing import List, Dict, Optional
import threading
import time

from memory_system import FantasyMemorySystem
from local_llm import LocalFantasyLLM, get_model_for_vram
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FantasyChatbot:
    def __init__(self, session_id: str = None, model_name: str = None, 
                 use_quantization: bool = True, memory_db_path: str = "fantasy_world.db"):
        """
        Initialize the fantasy chatbot with memory and LLM.
        
        Args:
            session_id: Unique session identifier for conversation history
            model_name: LLM model to use (auto-detects if None)
            use_quantization: Use model quantization to save VRAM
            memory_db_path: Path to SQLite database for memories
        """
        self.session_id = session_id or str(uuid.uuid4())
        self.memory_system = FantasyMemorySystem(memory_db_path)
        
        # Auto-detect GPU memory and recommend model
        if model_name is None:
            if self._has_cuda():
                import torch
                vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
                model_name = get_model_for_vram(vram_gb, use_quantization)
                logger.info(f"Auto-detected {vram_gb:.1f}GB VRAM, using model: {model_name}")
            else:
                model_name = "microsoft/DialoGPT-medium"  # Safe CPU fallback
                logger.info("Using CPU, defaulting to DialoGPT-medium")
        
        self.llm = LocalFantasyLLM(model_name)
        self.use_quantization = use_quantization
        
        # Initialize world with some default content if database is empty
        self._initialize_world_if_empty()
    
    def _has_cuda(self) -> bool:
        """Check if CUDA is available."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
    
    def _initialize_world_if_empty(self):
        """Initialize the fantasy world with default content if database is empty."""
        stats = self.memory_system.get_memory_stats()
        
        if stats['total_memories'] == 0:
            logger.info("Initializing new fantasy world...")
            
            # Store initial world setup
            self.memory_system.store_memory(
                "A vast fantasy realm where magic flows through ancient ley lines",
                "world",
                "The Realm",
                {"magic_level": "high", "technology_level": "medieval", "era": "age_of_legends"},
                importance=10
            )
            
            # Add a starting location
            self.memory_system.store_memory(
                "A bustling medieval town with cobblestone streets, timber-framed houses, and a grand tavern called 'The Prancing Pony'",
                "location", 
                "Havenbrook",
                {"type": "town", "population": "medium", "tech_level": "medieval"},
                importance=8
            )
            
            # Add some NPCs
            self.memory_system.store_memory(
                "Barkeep Thorin Oakenshield - a friendly dwarf with a red beard and a hearty laugh",
                "character",
                "Thorin",
                {"race": "dwarf", "role": "barkeeper", "personality": "friendly", "age": "middle-aged"},
                importance=7
            )
            
            # Set initial world state
            self.memory_system.set_world_state("current_time", "morning", "The sun is rising over Havenbrook")
            self.memory_system.set_world_state("weather", "clear", "A beautiful, crisp morning with light clouds")
            self.memory_system.set_world_state("mood", "peaceful", "The town is quiet and peaceful as people start their day")
            
            logger.info("World initialized with default content")
    
    def chat(self, user_input: str) -> Dict:
        """
        Main chat interface - process user input and generate response.
        
        Returns:
            Dict with response text and metadata
        """
        start_time = time.time()
        
        try:
            # Retrieve relevant memories
            relevant_memories = self.memory_system.retrieve_relevant_memories(user_input, limit=7)
            
            # Get world state
            world_state = self.memory_system.get_world_state()
            
            # Get recent conversation history
            conversation_history = self.memory_system.get_conversation_history(self.session_id, limit=5)
            
            # Generate response using LLM
            response = self.llm.generate_response(
                user_input=user_input,
                relevant_memories=relevant_memories,
                world_state=world_state,
                conversation_history=conversation_history
            )
            
            # Auto-extract important memories from user input and response
            auto_extracted = self.memory_system.auto_extract_memories(user_input, response)
            
            # Extract and store new memories from the response (existing functionality)
            self._extract_and_store_memories(response, relevant_memories)
            
            # Store the conversation
            retrieved_memory_ids = [mem['id'] for mem in relevant_memories]
            self.memory_system.store_conversation(
                session_id=self.session_id,
                user_input=user_input,
                ai_response=response,
                retrieved_memory_ids=retrieved_memory_ids
            )
            
            # Update world state with time progression
            self._update_world_state_after_turn()
            
            processing_time = time.time() - start_time
            
            return {
                'response': response,
                'processing_time': processing_time,
                'memories_used': len(relevant_memories),
                'auto_extracted_memories': len(auto_extracted),
                'session_id': self.session_id,
                'memory_stats': self.memory_system.get_memory_stats()
            }
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return {
                'response': "I apologize, but I'm having trouble processing that right now. The magic seems to be disrupted...",
                'error': str(e),
                'processing_time': time.time() - start_time
            }
    
    def _extract_and_store_memories(self, response: str, context_memories: List[Dict]):
        """Extract new facts from the LLM response and store them as memories."""
        import re
        
        # Simple extraction patterns (can be enhanced with more sophisticated NLP)
        patterns = {
            'character': [
                r'(?:I meet|meet|see|encounter)\s+(?:a|an|the)?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,?\s*(.*?)(?:\.|\n)',
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:is|appears|seems)\s+(.*?)(?:\.|\n)',
                r'NPC:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[:\-]\s*(.*?)(?:\.|\n)'
            ],
            'location': [
                r'(?:go to|enter|arrive at|reach)\s+(?:the\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,?\s*(.*?)(?:\.|\n)',
                r'(?:Location|Place):\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[:\-]\s*(.*?)(?:\.|\n)'
            ],
            'item': [
                r'(?:find|discover|pick up|take)\s+(?:a|an|the)?\s*([A-Z][a-z]+(?:\s+[a-z]+)*)\s*,?\s*(.*?)(?:\.|\n)',
                r'(?:Item|Object):\s*([A-Z][a-z]+(?:\s+[a-z]+)*)\s*[:\-]\s*(.*?)(?:\.|\n)'
            ],
            'event': [
                r'(?:suddenly|then|afterwards)\s+(.*?)(?:\.|\n)',
                r'(?:Event|Incident):\s*(.*?)(?:\.|\n)'
            ]
        }
        
        extracted_count = 0
        for memory_type, type_patterns in patterns.items():
            for pattern in type_patterns:
                matches = re.finditer(pattern, response, re.IGNORECASE)
                for match in matches:
                    if memory_type in ['character', 'location', 'item']:
                        name = match.group(1).strip()
                        content = match.group(2).strip() if len(match.groups()) > 1 else ""
                        full_content = f"{name}: {content}" if content else name
                    else:  # event
                        full_content = match.group(1).strip()
                        name = full_content[:50] + "..." if len(full_content) > 50 else full_content
                    
                    # Avoid duplicating existing memories
                    if not self._memory_already_exists(full_content, context_memories):
                        self.memory_system.store_memory(
                            content=full_content,
                            memory_type=memory_type,
                            name=name,
                            importance=5  # Default importance
                        )
                        extracted_count += 1
        
        if extracted_count > 0:
            logger.info(f"Extracted and stored {extracted_count} new memories")
    
    def _memory_already_exists(self, content: str, existing_memories: List[Dict]) -> bool:
        """Check if a similar memory already exists."""
        content_lower = content.lower()
        for memory in existing_memories:
            if content_lower in memory['content'].lower() or memory['content'].lower() in content_lower:
                return True
        return False
    
    def _update_world_state_after_turn(self):
        """Update world state to reflect time progression after each turn."""
        # Simple time progression - can be enhanced
        current_states = self.memory_system.get_world_state("current_time")
        if current_states:
            last_time = current_states[0]['value']
            # Simple progression (could be made more sophisticated)
            if last_time == "morning":
                self.memory_system.set_world_state("current_time", "midday", "The sun is at its zenith")
            elif last_time == "midday":
                self.memory_system.set_world_state("current_time", "afternoon", "The afternoon shadows grow longer")
            elif last_time == "afternoon":
                self.memory_system.set_world_state("current_time", "evening", "The sun sets, painting the sky orange")
            elif last_time == "evening":
                self.memory_system.set_world_state("current_time", "night", "Stars twinkle in the darkening sky")
            elif last_time == "night":
                self.memory_system.set_world_state("current_time", "dawn", "Dawn breaks over the horizon")
    
    def get_memory_stats(self) -> Dict:
        """Get current memory statistics."""
        return self.memory_system.get_memory_stats()
    
    def get_memory_usage(self) -> Dict:
        """Get current LLM memory usage."""
        return self.llm.get_memory_usage()
    
    def search_memories(self, query: str, memory_type: str = None) -> List[Dict]:
        """Search memories by query and optionally by type."""
        if memory_type:
            memories = self.memory_system.get_memories_by_type(memory_type, limit=20)
            # Filter by relevance
            relevant = []
            for mem in memories:
                if query.lower() in mem['content'].lower() or query.lower() in (mem['name'] or "").lower():
                    relevant.append(mem)
            return relevant
        else:
            return self.memory_system.retrieve_relevant_memories(query, limit=20)


def run_cli(chatbot: FantasyChatbot):
    """Run the command-line interface."""
    print("=== Persistent Fantasy Chatbot ===")
    print("Welcome to your persistent fantasy world!")
    print("Type 'quit', 'exit', or 'help' for commands.")
    print("Your memories will persist between sessions.")
    print("=" * 40)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Farewell! Your world will remember this adventure.")
                break
            
            if user_input.lower() == 'help':
                print("\nCommands:")
                print("- Type naturally to interact with the world")
                print("- 'stats' - Show memory and performance statistics")
                print("- 'search <query>' - Search your memories")
                print("- 'memories [type]' - Show recent memories (optionally by type)")
                print("- 'world' - Show current world state")
                print("- 'quit' - Exit the chatbot")
                continue
            
            if user_input.lower() == 'stats':
                stats = chatbot.get_memory_stats()
                memory_usage = chatbot.get_memory_usage()
                print(f"\nMemory Stats: {json.dumps(stats, indent=2)}")
                print(f"LLM Memory: {json.dumps(memory_usage, indent=2)}")
                continue
            
            if user_input.lower().startswith('search '):
                query = user_input[7:].strip()
                results = chatbot.search_memories(query)
                print(f"\nSearch results for '{query}':")
                for i, mem in enumerate(results[:5], 1):
                    print(f"{i}. [{mem['type']}] {mem['name']}: {mem['content']}")
                continue
            
            if user_input.lower().startswith('memories'):
                parts = user_input.split(' ', 1)
                memory_type = parts[1].strip() if len(parts) > 1 else None
                memories = chatbot.memory_system.get_memories_by_type(memory_type or 'character', limit=10)
                print(f"\nRecent {'all' if not memory_type else memory_type} memories:")
                for i, mem in enumerate(memories, 1):
                    print(f"{i}. [{mem['type']}] {mem['name']}: {mem['content']}")
                continue
            
            if user_input.lower() == 'world':
                world_state = chatbot.memory_system.get_world_state()
                print("\nCurrent World State:")
                for state in world_state[-10:]:
                    print(f"- {state['key']}: {state['value']}")
                continue
            
            # Regular conversation
            result = chatbot.chat(user_input)
            print(f"\nAI: {result['response']}")
            
            # Show some stats for long responses
            if result.get('memories_used', 0) > 0:
                print(f"(Used {result['memories_used']} memories, processed in {result['processing_time']:.2f}s)")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Persistent Fantasy Chatbot")
    parser.add_argument('--model', type=str, help='LLM model to use')
    parser.add_argument('--no-quantization', action='store_true', help='Disable model quantization')
    parser.add_argument('--db-path', type=str, default='fantasy_world.db', help='Path to memory database')
    parser.add_argument('--session-id', type=str, help='Session ID for conversation continuity')
    parser.add_argument('--load-model-only', action='store_true', help='Only load the model without starting chat')
    
    args = parser.parse_args()
    
    # Initialize chatbot
    chatbot = FantasyChatbot(
        session_id=args.session_id,
        model_name=args.model,
        use_quantization=not args.no_quantization,
        memory_db_path=args.db_path
    )
    
    # Load the LLM model
    print("Loading local LLM model...")
    chatbot.llm.load_model(quantization_4bit=chatbot.use_quantization)
    
    if args.load_model_only:
        print("Model loaded successfully!")
        print(f"Memory usage: {chatbot.get_memory_usage()}")
        return
    
    # Start CLI interface
    run_cli(chatbot)


if __name__ == "__main__":
    main()