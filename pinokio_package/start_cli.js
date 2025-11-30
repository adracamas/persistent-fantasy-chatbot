{
  "version": "4.0",
  "run": [
    {
      "method": "shell.run",
      "params": {
        "venv": "env",
        "message": "echo '🎮 Starting Fantasy Chatbot - God Mode Edition'",
        "path": "."
      }
    },
    {
      "method": "shell.run", 
      "params": {
        "venv": "env",
        "message": "python fantasy_chatbot.py",
        "path": ".",
        "input": true
      }
    }
  ],
  "daemon": false,
  "env": [
    {
      "name": "FANTASY_CHATBOT_MODE",
      "value": "cli"
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
  }
}