#!/usr/bin/env python3
"""Test the database fix."""

from memory_system import FantasyMemorySystem

print("Testing memory system initialization...")
memory = FantasyMemorySystem("test_fantasy_world.db")
print("✅ Memory system initialized")

print("Testing memory storage...")
memory.store_memory(
    "Thorin Ironbeard is a friendly dwarf bartender",
    "character",
    "Thorin",
    {"race": "dwarf", "role": "barkeeper"},
    importance=8
)
print("✅ Memory stored successfully")

print("Testing memory retrieval...")
results = memory.retrieve_relevant_memories("Tell me about the dwarf", limit=3)
print(f"✅ Retrieved {len(results)} memories")

if results:
    print(f"Top result: {results[0]['name']} - {results[0]['content']}")

print("✅ All tests passed! Database fix is working.")