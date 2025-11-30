{
  "version": "4.0",
  "run": [
    {
      "method": "shell.run",
      "params": {
        "venv": "env",
        "message": "echo '🧠 Fantasy Memory System Management'",
        "input": true
      }
    },
    {
      "method": "shell.run",
      "params": {
        "venv": "env",
        "message": "python -c \"\nimport sys\nsys.path.insert(0, '.')\nfrom memory_system import FantasyMemorySystem\nimport json\n\nmemory = FantasyMemorySystem()\n\nprint('=== MEMORY STATISTICS ===')\nstats = memory.get_memory_stats()\nprint(json.dumps(stats, indent=2))\n\nprint('\\n=== RECENT MEMORIES ===')\nrecent = memory.get_memories_by_type('character', limit=5)\nprint('Recent Characters:')\nfor mem in recent:\n    print(f'- {mem[\\\"name\\\"]}: {mem[\\\"content\\\"]}')\n\nrecent = memory.get_memories_by_type('location', limit=5)\nprint('Recent Locations:')\nfor mem in recent:\n    print(f'- {mem[\\\"name\\\"]}: {mem[\\\"content\\\"]}')\n\""
      }
    },
    {
      "method": "shell.run",
      "params": {
        "venv": "env", 
        "message": "echo '\\n=== SEARCH MEMORIES ===' && python -c \"\nimport sys\nsys.path.insert(0, '.')\nfrom memory_system import FantasyMemorySystem\n\nmemory = FantasyMemorySystem()\nquery = input('Enter search query: ')\nresults = memory.retrieve_relevant_memories(query, limit=10)\nprint(f'Found {len(results)} relevant memories:')\nfor i, mem in enumerate(results, 1):\n    print(f'{i}. [{mem[\\\"type\\\"]}] {mem[\\\"name\\\"]}: {mem[\\\"content\\\"]}')\n\""
      }
    }
  ],
  "daemon": false,
  "env": [
    {
      "name": "FANTASY_CHATBOT_MODE", 
      "value": "memory-manager"
    }
  ]
}