{
  "version": "4.0",
  "run": [
    {
      "method": "shell.run",
      "params": {
        "venv": "env",
        "message": "echo '🌐 Starting Web Interface for Fantasy Chatbot'"
      }
    },
    {
      "method": "shell.run",
      "params": {
        "venv": "env", 
        "message": "python web_interface.py --host 0.0.0.0 --port {{port}}",
        "path": ".",
        "input": false
      }
    }
  ],
  "daemon": true,
  "env": [
    {
      "name": "FANTASY_CHATBOT_MODE",
      "value": "web"
    },
    {
      "name": "PYTORCH_CUDA_ALLOC_CONF", 
      "value": "max_split_size_mb:512"
    }
  ],
  "cache": {
    "transformers": "~/.cache/huggingface",
    "torch": "~/.cache/torch", 
    "sentencetransformers": "~/.cache/sentence_transformers"
  },
  "on": [
    {
      "match": "INFO:.*Uvicorn running on http://0.0.0.0",
      "action": "done",
      "href": "http://localhost:{{port}}"
    }
  ]
}