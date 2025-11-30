"""
Fantasy World Memory System
Handles persistent storage and retrieval of world state using SQLite and embeddings.
"""

import sqlite3
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FantasyMemorySystem:
    def __init__(self, db_path: str = "fantasy_world.db"):
        self.db_path = db_path
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database with necessary tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main memory store
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,  -- character, location, item, event, dialogue
                name TEXT,
                content TEXT NOT NULL,
                attributes TEXT,  -- JSON string for additional attributes
                embedding BLOB,  -- Serialized embedding vector
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                importance INTEGER DEFAULT 5,  -- 1-10 scale
                context TEXT  -- Additional context information
            )
        ''')
        
        # Conversations history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                user_input TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                retrieved_memories TEXT,  -- JSON array of memory IDs used
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # World state tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS world_state (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                state_type TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                description TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_memories_timestamp ON memories(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_session ON conversations(session_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_world_state_type ON world_state(state_type)')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def _ensure_tables_exist(self):
        """Ensure all required tables exist before database operations."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if memories table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='memories'")
        if not cursor.fetchone():
            logger.info("Tables not found, reinitializing database...")
            self._init_database()
            return
            
        conn.close()
    
    def store_memory(self, content: str, memory_type: str, name: str = None, 
                    attributes: Dict = None, importance: int = 5, context: str = None) -> str:
        """Store a new memory with automatic embedding generation."""
        # Ensure tables exist
        self._ensure_tables_exist()
        
        memory_id = str(uuid.uuid4())
        
        # Generate embedding
        embedding = self.embedder.encode([content])[0]
        embedding_bytes = embedding.tobytes()
        
        # Serialize attributes
        attributes_json = json.dumps(attributes) if attributes else None
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO memories (id, type, name, content, attributes, embedding, importance, context)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (memory_id, memory_type, name, content, attributes_json, embedding_bytes, importance, context))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Stored memory: {memory_id} ({memory_type})")
        return memory_id
    
    def auto_extract_memories(self, user_input: str, ai_response: str = None) -> List[str]:
        """
        Automatically extract and store important memories from user input and AI response.
        This helps maintain the god-like control by remembering key story elements.
        """
        stored_ids = []
        
        # Extract important entities and events from user input
        text_to_analyze = f"{user_input} {ai_response or ''}"
        
        # Look for character mentions (proper nouns that could be names)
        import re
        
        # Find potential character names (capitalized words)
        potential_names = re.findall(r'\b[A-Z][a-z]+\b', text_to_analyze)
        for name in potential_names[:3]:  # Limit to avoid over-storing
            if len(name) > 2 and name.lower() not in ['the', 'and', 'you', 'are', 'with', 'from']:
                # Check if this character isn't already stored
                existing_chars = self.get_memories_by_type("character")
                if not any(name.lower() in char['name'].lower() if char['name'] else False for char in existing_chars):
                    stored_id = self.store_memory(
                        f"{name} is mentioned in the story",
                        "character", 
                        name,
                        importance=6
                    )
                    stored_ids.append(stored_id)
        
        # Extract location mentions
        location_keywords = ['village', 'town', 'city', 'forest', 'mountain', 'castle', 'tavern', 'inn', 'palace', 'forest', 'river', 'lake']
        for keyword in location_keywords:
            if keyword in text_to_analyze.lower():
                # Try to find the full location name
                pattern = rf'(\b\w+\s+){keyword}\b'
                matches = re.findall(pattern, text_to_analyze.lower())
                if matches:
                    location_name = ' '.join(matches[0]).strip() + f" {keyword}"
                    if location_name not in [loc['name'] for loc in self.get_memories_by_type("location")]:
                        stored_id = self.store_memory(
                            f"{location_name} is mentioned in the story",
                            "location",
                            location_name.title(),
                            importance=5
                        )
                        stored_ids.append(stored_id)
        
        # Extract event/plot developments
        event_indicators = ['suddenly', 'meanwhile', 'however', 'unexpectedly', 'the next day', 'afterwards']
        for indicator in event_indicators:
            if indicator in text_to_analyze.lower():
                # Store significant plot moments
                stored_id = self.store_memory(
                    f"Plot development: {text_to_analyze[:100]}...",
                    "event",
                    importance=7
                )
                stored_ids.append(stored_id)
                break  # Only store one event per analysis
        
        return stored_ids
    
    def retrieve_relevant_memories(self, query: str, limit: int = 5) -> List[Dict]:
        """Retrieve memories relevant to the query using semantic similarity."""
        # Ensure tables exist
        self._ensure_tables_exist()
        
        # Generate query embedding
        query_embedding = self.embedder.encode([query])[0]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all memories with their embeddings
        cursor.execute('''
            SELECT id, type, name, content, attributes, embedding, importance, timestamp
            FROM memories
        ''')
        
        memories = cursor.fetchall()
        conn.close()
        
        # Calculate similarities
        similarities = []
        for memory in memories:
            memory_embedding = np.frombuffer(memory[5], dtype=np.float32)
            similarity = np.dot(query_embedding, memory_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(memory_embedding)
            )
            
            # Weight by importance
            weighted_similarity = similarity * (memory[6] / 10.0)
            
            similarities.append({
                'id': memory[0],
                'type': memory[1],
                'name': memory[2],
                'content': memory[3],
                'attributes': json.loads(memory[4]) if memory[4] else None,
                'importance': memory[6],
                'timestamp': memory[7],
                'similarity': weighted_similarity
            })
        
        # Sort by weighted similarity and return top results
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:limit]
    
    def get_memories_by_type(self, memory_type: str, limit: int = 50) -> List[Dict]:
        """Retrieve memories of a specific type."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, type, name, content, attributes, importance, timestamp
            FROM memories
            WHERE type = ?
            ORDER BY importance DESC, timestamp DESC
            LIMIT ?
        ''', (memory_type, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'id': row[0],
            'type': row[1],
            'name': row[2],
            'content': row[3],
            'attributes': json.loads(row[4]) if row[4] else None,
            'importance': row[5],
            'timestamp': row[6]
        } for row in results]
    
    def store_conversation(self, session_id: str, user_input: str, ai_response: str, 
                          retrieved_memory_ids: List[str] = None):
        """Store a conversation exchange."""
        conversation_id = str(uuid.uuid4())
        retrieved_memories_json = json.dumps(retrieved_memory_ids) if retrieved_memory_ids else None
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (id, session_id, user_input, ai_response, retrieved_memories)
            VALUES (?, ?, ?, ?, ?)
        ''', (conversation_id, session_id, user_input, ai_response, retrieved_memories_json))
        
        conn.commit()
        conn.close()
    
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Retrieve conversation history for a session."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_input, ai_response, timestamp
            FROM conversations
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (session_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'user_input': row[0],
            'ai_response': row[1],
            'timestamp': row[2]
        } for row in results[::-1]]  # Reverse to get chronological order
    
    def set_world_state(self, state_type: str, key: str, value: str, description: str = None):
        """Set or update world state information."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO world_state (state_type, key, value, description)
            VALUES (?, ?, ?, ?)
        ''', (state_type, key, value, description))
        
        conn.commit()
        conn.close()
    
    def get_world_state(self, state_type: str = None) -> List[Dict]:
        """Get world state information."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if state_type:
            cursor.execute('''
                SELECT state_type, key, value, description, timestamp
                FROM world_state
                WHERE state_type = ?
                ORDER BY timestamp DESC
            ''', (state_type,))
        else:
            cursor.execute('''
                SELECT state_type, key, value, description, timestamp
                FROM world_state
                ORDER BY timestamp DESC
            ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'state_type': row[0],
            'key': row[1],
            'value': row[2],
            'description': row[3],
            'timestamp': row[4]
        } for row in results]
    
    def get_memory_stats(self) -> Dict:
        """Get statistics about stored memories."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count by type
        cursor.execute('SELECT type, COUNT(*) FROM memories GROUP BY type')
        type_counts = dict(cursor.fetchall())
        
        # Total count
        cursor.execute('SELECT COUNT(*) FROM memories')
        total_count = cursor.fetchone()[0]
        
        # Recent memories (last 24 hours)
        cursor.execute('SELECT COUNT(*) FROM memories WHERE timestamp > datetime("now", "-1 day")')
        recent_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_memories': total_count,
            'by_type': type_counts,
            'recent_memories': recent_count
        }


# Test the memory system
if __name__ == "__main__":
    memory = FantasyMemorySystem()
    
    # Store some example memories
    memory.store_memory(
        "Eldara the Elf Queen rules from her crystal palace in the Skylands",
        "character",
        "Eldara",
        {"race": "elf", "role": "queen", "location": "Skylands"},
        importance=9
    )
    
    memory.store_memory(
        "The Ancient Forest of Whispering Trees lies east of the village",
        "location",
        "Ancient Forest",
        {"type": "forest", "mysterious": True, "danger_level": "moderate"},
        importance=7
    )
    
    # Test retrieval
    relevant = memory.retrieve_relevant_memories("Tell me about the queen", limit=3)
    print("Relevant memories:")
    for mem in relevant:
        print(f"- {mem['name']}: {mem['content']} (similarity: {mem['similarity']:.3f})")
    
    # Print statistics
    stats = memory.get_memory_stats()
    print(f"\nMemory statistics: {stats}")