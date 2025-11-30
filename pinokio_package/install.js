{
  "version": "4.0",
  "run": [
    {
      "method": "shell.run",
      "params": {
        "venv": "env",
        "message": "echo '🔍 Checking system requirements...'"
      }
    },
    {
      "method": "shell.run",
      "params": {
        "venv": "env",
        "message": "python check_system.py"
      }
    },
    {
      "method": "shell.run",
      "params": {
        "venv": "env",
        "message": "echo '📦 Installing Python dependencies...'"
      }
    },
    {
      "method": "shell.run",
      "params": {
        "venv": "env",
        "message": "pip install --upgrade pip"
      }
    },
    {
      "method": "shell.run",
      "params": {
        "venv": "env",
        "message": "pip install -r requirements.txt"
      }
    },
    {
      "method": "shell.run",
      "params": {
        "venv": "env",
        "message": "echo '✅ Verifying installation...'"
      }
    },
    {
      "method": "shell.run",
      "params": {
        "venv": "env",
        "message": "pip list"
      }
    },
    {
      "method": "shell.run",
      "params": {
        "venv": "env",
        "message": "python setup.py --test-only"
      }
    },
    {
      "method": "shell.run",
      "params": {
        "venv": "env",
        "message": "python -c \"import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \\\"CPU\\\"}')\""
      }
    }
  ],
  "daemon": false,
  "env": [
    {
      "name": "PYTORCH_CUDA_ALLOC_CONF", 
      "value": "max_split_size_mb:512",
      "description": "PyTorch CUDA memory configuration"
    }
  ],
  "on": [
    {
      "match": "Successfully installed",
      "action": "done"
    },
    {
      "match": "ERROR|error|failed",
      "action": "break"
    }
  ]
}