{
  "version": "4.0",
  "run": [
    {
      "method": "shell.run",
      "params": {
        "venv": "env",
        "message": "echo '📊 Fantasy Chatbot System Statistics' && echo '================================='"
      }
    },
    {
      "method": "shell.run",
      "params": {
        "venv": "env",
        "message": "python -c \"\nimport sys\nsys.path.insert(0, '.')\nimport torch\nimport sqlite3\nimport os\n\nprint('\\n🔧 SYSTEM INFORMATION:')\nprint(f'Python: {sys.version.split()[0]}')\nprint(f'PyTorch: {torch.__version__}')\nprint(f'CUDA Available: {torch.cuda.is_available()}')\n\nif torch.cuda.is_available():\n    print(f'GPU: {torch.cuda.get_device_name(0)}')\n    print(f'GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB')\n    print(f'CUDA Version: {torch.version.cuda}')\n\nprint('\\n💾 DATABASE STATUS:')\ndb_files = ['fantasy_world.db', 'demo_fantasy_world.db']\nfor db_file in db_files:\n    if os.path.exists(db_file):\n        conn = sqlite3.connect(db_file)\n        cursor = conn.cursor()\n        cursor.execute('SELECT COUNT(*) FROM memories')\n        memory_count = cursor.fetchone()[0]\n        conn.close()\n        print(f'{db_file}: {memory_count} memories stored')\n    else:\n        print(f'{db_file}: Not created yet')\n\nprint('\\n📁 PROJECT FILES:')\nproject_files = [\n    'fantasy_chatbot.py',\n    'memory_system.py', \n    'local_llm.py',\n    'web_interface.py',\n    'setup.py',\n    'requirements.txt'\n]\n\nfor file in project_files:\n    status = '✅' if os.path.exists(file) else '❌'\n    print(f'{status} {file}')\n\""
      }
    },
    {
      "method": "shell.run", 
      "params": {
        "venv": "env",
        "message": "echo '\\n🚀 PERFORMANCE TEST:' && python -c \"\nimport sys\nsys.path.insert(0, '.')\nfrom sentence_transformers import SentenceTransformer\nimport time\n\nprint('Testing embedding model loading...')\nstart = time.time()\nmodel = SentenceTransformer('all-MiniLM-L6-v2')\nload_time = time.time() - start\n\nprint(f'Embedding model loaded in {load_time:.2f} seconds')\n\nprint('Testing embedding generation...')\nstart = time.time()\nembedding = model.encode('Test sentence for fantasy chatbot')\ngen_time = time.time() - start\n\nprint(f'Embedding generated in {gen_time:.3f} seconds')\nprint(f'Embedding dimensions: {len(embedding)}')\n\""
      }
    }
  ],
  "daemon": false
}