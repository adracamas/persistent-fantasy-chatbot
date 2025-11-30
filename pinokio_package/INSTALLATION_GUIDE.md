# 🚀 Installation Guide - Complete Self-Containment

## 📋 **What You Need (Minimum Requirements)**

### 🔧 **System Requirements**
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8+ (Pinokio handles this automatically)
- **GPU**: NVIDIA GPU with 12GB+ VRAM (RTX 5070, RTX 4080, etc.) OR CPU-only mode
- **RAM**: 8GB+ system memory
- **Storage**: 20GB+ free space for models and dependencies

### 📦 **What's Included (100% Self-Contained)**
✅ **All Python Dependencies**: Via pip from requirements.txt  
✅ **Application Code**: Complete source code  
✅ **Hardware Detection**: Auto-optimizes for your system  
✅ **Model Downloads**: Automatic via HuggingFace  
✅ **Database Setup**: SQLite with vector embeddings  
✅ **Web Interface**: Complete static files included  

### 🔄 **What Pinokio Provides**
- **Python Runtime**: Managed by Pinokio
- **Virtual Environment**: Isolated `env/` directory
- **Dependency Management**: Automatic pip installation
- **Process Management**: Daemon services for web interface

## 🎯 **Two Installation Options**

### Option 1: Pinokio (Recommended - Easiest)

**One-click installation with zero manual setup:**

1. **Download Pinokio Launcher**
   ```
   Visit: https://pinokio.co
   Download and install Pinokio Launcher
   ```

2. **Install Fantasy Chatbot**
   ```
   - Search for "Persistent Fantasy Chatbot" in Pinokio
   - OR paste your GitHub repository URL
   - Click "Install"
   ```

3. **Pinokio Handles Everything**
   ```
   ✅ Creates isolated Python environment
   ✅ Installs all dependencies via pip
   ✅ Downloads and configures AI models
   ✅ Sets up database and web interface
   ✅ Creates optimized launchers
   ```

### Option 2: Manual Installation (Advanced)

**For users who prefer manual control or don't use Pinokio:**

```bash
# 1. Create virtual environment
python -m venv fantasy_env
source fantasy_env/bin/activate  # Windows: fantasy_env\Scripts\activate

# 2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Run system check
python check_system.py

# 4. Setup and test
python setup.py

# 5. Launch
python fantasy_chatbot.py  # CLI mode
python web_interface.py    # Web mode
```

## 🔍 **System Requirements Verification**

### Automatic Check (via Pinokio)
Pinokio automatically runs our system check script:
- Verifies Python installation
- Checks NVIDIA drivers
- Validates CUDA availability
- Confirms GPU memory requirements

### Manual Check (if needed)
```bash
python check_system.py
```

This checks:
- Python 3.8+
- pip availability
- NVIDIA drivers
- CUDA/PyTorch compatibility
- GPU memory requirements

## 🛠️ **Dependency Details**

### **Core AI/ML Stack**
```
torch>=2.0.0           # PyTorch deep learning framework
torchvision>=0.15.0    # Computer vision utilities
torchaudio>=2.0.0      # Audio processing
transformers>=4.30.0   # HuggingFace transformers
bitsandbytes>=0.41.0   # Model quantization
accelerate>=0.20.0     # Training acceleration
sentence-transformers>=2.2.2  # Vector embeddings
```

### **Web Interface**
```
fastapi>=0.100.0       # Modern web framework
uvicorn>=0.23.0        # ASGI server
streamlit>=1.25.0      # Dashboard framework
```

### **Data Processing**
```
numpy>=1.24.0          # Numerical computing
pandas>=2.0.0          # Data manipulation
scikit-learn>=1.3.0    # Machine learning utilities
```

### **Utilities**
```
python-dotenv>=1.0.0   # Environment variables
requests>=2.31.0       # HTTP client
chromadb>=0.4.0        # Vector database
langchain>=0.1.0       # LLM application framework
```

## 🎮 **Hardware Optimization**

### **RTX 5070 (12GB VRAM) - Optimized**
- **Model**: Llama-2-7B (4-bit quantized)
- **Memory Usage**: ~4GB VRAM
- **Performance**: 15-25 tokens/second
- **Cold Start**: 30-60 seconds

### **High-End GPUs (16GB+ VRAM)**
- **Model**: Llama-2-13B (4-bit quantized) 
- **Memory Usage**: ~6GB VRAM
- **Performance**: 20-30 tokens/second
- **Quality**: Higher due to larger model

### **CPU-Only Mode**
- **Model**: DialoGPT-medium (CPU optimized)
- **Memory Usage**: ~4GB RAM
- **Performance**: 2-5 tokens/second
- **Use Case**: Testing, low-end hardware

## 📱 **Platform-Specific Notes**

### **Windows**
- Requires Visual C++ Redistributables (usually pre-installed)
- NVIDIA drivers from: https://www.nvidia.com/drivers
- Windows 10/11 recommended

### **macOS**
- Apple Silicon (M1/M2) supported via CPU mode
- NVIDIA GPUs not supported (use CPU mode)
- macOS 10.15+ required

### **Linux**
- Ubuntu 18.04+ recommended
- NVIDIA drivers: `sudo apt install nvidia-driver-470` (or newer)
- CUDA Toolkit: Usually included with drivers

## 🔧 **Troubleshooting Installation**

### **Common Issues & Solutions**

**"Python not found"**
```bash
# Install Python 3.8+ from python.org
# Or use a version manager like pyenv
```

**"pip not found"**
```bash
# Usually comes with Python
# If missing, install: python -m ensurepip --upgrade
```

**"CUDA out of memory"**
```bash
# Use smaller model
python fantasy_chatbot.py --model "microsoft/DialoGPT-large"

# Or enable quantization
python fantasy_chatbot.py --model "llama-2-7b"  # Auto-quantizes
```

**"NVIDIA drivers missing"**
```bash
# Windows: Download from NVIDIA website
# Linux: sudo apt install nvidia-driver-470
# macOS: CPU mode only (no NVIDIA support)
```

**"Model download fails"**
```bash
# Check internet connection
# Clear cache: rm -rf ~/.cache/huggingface/
# Restart installation
```

## 🌐 **Network Requirements**

- **Initial Setup**: ~2GB download (dependencies)
- **Model Download**: ~4-8GB (depending on model)
- **Runtime**: No internet required (everything local)

## 📊 **Storage Breakdown**

```
Total: ~15-20GB
├── Python Environment: ~2GB
├── AI Models: ~4-8GB  
├── Application Code: ~50MB
├── Database: ~100MB (grows with usage)
└── System Cache: ~1GB
```

## ✅ **Verification Checklist**

After installation, verify everything works:

```bash
# 1. Check Python environment
python --version  # Should be 3.8+

# 2. Verify dependencies
python -c "import torch, transformers; print('OK')"

# 3. Test GPU (if available)
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# 4. Run system check
python check_system.py

# 5. Test application
python fantasy_chatbot.py --help
```

## 🎯 **Summary: What's Truly Self-Contained**

✅ **Everything included in package**:  
- All Python code and dependencies
- Complete web interface
- Hardware detection and optimization
- Model downloading and management
- Database setup and management

✅ **Automatic via Pinokio**:
- Python installation and management
- Virtual environment creation
- Dependency resolution and installation
- Process management and daemon services

✅ **User only needs**:
- Pinokio Launcher (single download)
- NVIDIA GPU drivers (system requirement)
- Basic OS (Windows/macOS/Linux)

**Result**: True one-click installation with zero manual dependency management! 🚀