{
  "version": "4.0",
  "run": [
    {
      "method": "shell.run",
      "params": {
        "message": "echo '🔧 Fantasy Chatbot Configuration' && echo '=============================='"
      }
    },
    {
      "method": "shell.run",
      "params": {
        "venv": "env",
        "message": "python -c \"\nimport sys\nsys.path.insert(0, '.')\n\nprint('\\n🤖 AI MODEL CONFIGURATION:')\nprint('Current settings in local_llm.py:')\n\n# Show current configuration\nwith open('local_llm.py', 'r') as f:\n    content = f.read()\n    if 'temperature = 0.7' in content:\n        print('✅ Temperature: 0.7 (balanced creativity)')\n    if 'max_new_tokens = 512' in content:\n        print('✅ Max Tokens: 512 (optimal response length)')\n    if 'top_p = 0.85' in content:\n        print('✅ Top-p: 0.85 (focused generation)')\n\nprint('\\n📝 CONFIGURATION OPTIONS:')\nprint('1. GPU Configuration: Auto-detected based on available hardware')\nprint('2. Model Size: DialoGPT-medium (863MB) - good for testing')\nprint('3. Memory System: SQLite with vector embeddings (unlimited capacity)')\nprint('4. God-Like Control: Enabled (AI has full authority)')\nprint('5. Auto-Memory Extraction: Enabled')\n\nprint('\\n⚡ PERFORMANCE NOTES:')\nprint('- RTX 5070 (12GB): Can run Llama-2-7B (4-bit quantized)')\nprint('- RTX 4070 (12GB): Can run Llama-2-7B (4-bit quantized)')\nprint('- RTX 3070 (8GB): DialoGPT-medium recommended')\nprint('- CPU Only: DialoGPT-medium (slower but functional)')\n\""
      }
    },
    {
      "method": "shell.run",
      "params": {
        "message": "echo '\\n🗺️ MEMORY SYSTEM STATUS:' && python -c \"\nimport sys\nsys.path.insert(0, '.')\nfrom memory_system import FantasyMemorySystem\n\nmemory = FantasyMemorySystem()\nstats = memory.get_memory_stats()\n\nprint(f'Total Memories: {stats[\\\"total_memories\\\"]}')\nprint(f'By Type: {stats[\\\"by_type\\\"]}')\nprint(f'Recent (24h): {stats[\\\"recent_memories\\\"]}')\n\nprint('\\n📋 MEMORY TYPES SUPPORTED:')\nprint('- Characters: NPCs, heroes, creatures')\nprint('- Locations: Places, buildings, regions')\nprint('- Items: Objects, weapons, artifacts') \nprint('- Events: Plot points, battles, discoveries')\nprint('- Dialogue: Important conversations')\n\""
      }
    }
  ],
  "daemon": false,
  "env": [
    {
      "name": "FANTASY_CHATBOT_CONFIG_MODE",
      "value": "true"
    }
  ]
}