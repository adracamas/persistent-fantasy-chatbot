#!/usr/bin/env python3
"""
Setup and Launch Script for Fantasy Chatbot
Automatically detects hardware and configures optimal settings
"""

import os
import sys
import argparse
import subprocess
import json
from pathlib import Path

def check_requirements():
    """Check if required packages are installed."""
    required_packages = [
        'torch', 'transformers', 'bitsandbytes', 'sentence-transformers',
        'fastapi', 'uvicorn', 'numpy', 'pandas'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def check_gpu():
    """Check GPU availability and memory."""
    try:
        import torch
        
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            memory_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
            
            print(f"✅ GPU detected: {gpu_name}")
            print(f"   Memory: {memory_gb:.1f}GB")
            print(f"   Devices: {gpu_count}")
            
            return {
                'available': True,
                'count': gpu_count,
                'name': gpu_name,
                'memory_gb': memory_gb,
                'compute_capability': torch.cuda.get_device_capability(0)
            }
        else:
            print("⚠️  No GPU detected, will use CPU (much slower)")
            return {'available': False}
            
    except ImportError:
        print("❌ PyTorch not installed")
        return None

def recommend_model(gpu_info):
    """Recommend optimal model based on hardware."""
    if not gpu_info or not gpu_info.get('available'):
        return "microsoft/DialoGPT-medium"
    
    memory_gb = gpu_info['memory_gb']
    
    if memory_gb >= 16:
        print("🎯 Recommended model: Llama-2-13B (4-bit quantized)")
        return "meta-llama/Llama-2-13b-chat-hf"
    elif memory_gb >= 12:
        print("🎯 Recommended model: Llama-2-7B (4-bit quantized)")
        return "meta-llama/Llama-2-7b-chat-hf"
    elif memory_gb >= 8:
        print("🎯 Recommended model: DialoGPT-XL")
        return "microsoft/DialoGPT-xl"
    elif memory_gb >= 4:
        print("🎯 Recommended model: DialoGPT-Large")
        return "microsoft/DialoGPT-large"
    else:
        print("🎯 Recommended model: DialoGPT-Medium (CPU)")
        return "microsoft/DialoGPT-medium"

def setup_database():
    """Initialize the memory database."""
    try:
        from memory_system import FantasyMemorySystem
        memory = FantasyMemorySystem()
        
        # Check if database already exists and has content
        stats = memory.get_memory_stats()
        if stats['total_memories'] > 0:
            print(f"✅ Database initialized with {stats['total_memories']} existing memories")
        else:
            print("✅ New database created")
            
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def test_model_loading(model_name, use_quantization=True):
    """Test if model can be loaded with given settings."""
    try:
        from local_llm import LocalFantasyLLM
        
        print(f"🧪 Testing model: {model_name}")
        llm = LocalFantasyLLM(model_name)
        llm.load_model(quantization_4bit=use_quantization)
        
        # Test a simple generation
        response = llm.generate_response("Hello")
        
        print("✅ Model loaded and tested successfully")
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def create_launcher_script(gpu_info, recommended_model):
    """Create a launcher script with optimal settings."""
    launcher_content = f"""#!/usr/bin/env python3
# Auto-generated launcher for Fantasy Chatbot
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Auto-detected settings
GPU_AVAILABLE = {gpu_info.get('available', False) if gpu_info else False}
RECOMMENDED_MODEL = "{recommended_model}"
USE_QUANTIZATION = {gpu_info.get('available', False) if gpu_info else False} and {gpu_info.get('memory_gb', 0) < 16 if gpu_info else True}

print("🚀 Launching Fantasy Chatbot with optimal settings...")
print(f"Model: {{RECOMMENDED_MODEL}}")
print(f"Quantization: {{USE_QUANTIZATION}}")
print(f"GPU: {{GPU_AVAILABLE}}")

if len(sys.argv) > 1 and sys.argv[1] == "--web":
    # Launch web interface
    from web_interface import start_web_server
    start_web_server(
        model_name=RECOMMENDED_MODEL,
        use_quantization=USE_QUANTIZATION,
        auto_initialize=True
    )
else:
    # Launch CLI interface
    from fantasy_chatbot import FantasyChatbot, main
    import argparse
    
    parser = argparse.ArgumentParser(description="Fantasy Chatbot")
    parser.add_argument('--model', default=RECOMMENDED_MODEL, help='LLM model to use')
    parser.add_argument('--no-quantization', action='store_true', 
                       help='Disable model quantization')
    parser.add_argument('--session-id', help='Session ID for conversation continuity')
    
    args = parser.parse_args()
    
    # Override quantization setting if requested
    if args.no_quantization:
        use_quantization = False
    
    chatbot = FantasyChatbot(
        session_id=args.session_id,
        model_name=args.model,
        use_quantization=use_quantization
    )
    
    print("📥 Loading model... (this may take a few minutes on first run)")
    chatbot.llm.load_model(quantization_4bit=use_quantization)
    
    from fantasy_chatbot import run_cli
    run_cli(chatbot)
"""
    
    with open('launch_chatbot.py', 'w') as f:
        f.write(launcher_content)
    
    # Make executable on Unix systems
    if os.name != 'nt':
        os.chmod('launch_chatbot.py', 0o755)
    
    print("✅ Created launcher script: launch_chatbot.py")

def print_usage_instructions():
    """Print instructions for using the chatbot."""
    print("\n" + "="*60)
    print("🎮 FANTASY CHATBOT SETUP COMPLETE!")
    print("="*60)
    print()
    print("Quick Start:")
    print("  python launch_chatbot.py              # CLI interface")
    print("  python launch_chatbot.py --web        # Web interface")
    print()
    print("Manual Launch:")
    print("  python fantasy_chatbot.py             # CLI with custom args")
    print("  python web_interface.py               # Web server only")
    print()
    print("Web Interface Features:")
    print("  • Real-time chat with WebSocket")
    print("  • Memory search and exploration")
    print("  • World state tracking")
    print("  • Session statistics")
    print()
    print("CLI Features:")
    print("  • Persistent conversation history")
    print("  • Memory management commands")
    print("  • World exploration tools")
    print()
    print("Files Created:")
    print("  • fantasy_world.db - Your persistent world memory")
    print("  • launch_chatbot.py - Optimized launcher")
    print()
    print("First Run Tips:")
    print("  1. The model will download on first use (could take several GB)")
    print("  2. Start with simple descriptions to build your world")
    print("  3. Use 'help' command in CLI for available commands")
    print("  4. Your world persists between sessions!")
    print()
    print("Enjoy your persistent fantasy adventure! 🏰✨")
    print("="*60)

def main():
    parser = argparse.ArgumentParser(description="Setup Fantasy Chatbot")
    parser.add_argument('--test-only', action='store_true', 
                       help='Only test hardware and models without setup')
    parser.add_argument('--model', type=str, help='Specify model to use')
    parser.add_argument('--no-gpu', action='store_true', help='Force CPU mode')
    parser.add_argument('--skip-model-test', action='store_true', 
                       help='Skip model loading test')
    
    args = parser.parse_args()
    
    print("🔧 Fantasy Chatbot Setup")
    print("="*40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]}")
    
    # Check requirements
    print("📦 Checking requirements...")
    if not check_requirements():
        sys.exit(1)
    
    # Check GPU
    print("🖥️  Checking hardware...")
    gpu_info = check_gpu()
    
    if args.no_gpu:
        gpu_info = {'available': False}
        print("🔧 Forced CPU mode")
    
    # Recommend model
    if args.model:
        recommended_model = args.model
        print(f"🎯 Using specified model: {recommended_model}")
    else:
        recommended_model = recommend_model(gpu_info)
    
    # Setup database
    print("🗄️  Setting up database...")
    if not setup_database():
        sys.exit(1)
    
    # Test model (if not skipped)
    if not args.skip_model_test:
        print("🧪 Testing model loading...")
        if test_model_loading(recommended_model, gpu_info.get('available', False)):
            print("✅ Model test passed")
        else:
            print("⚠️  Model test failed, but continuing with setup")
    
    # Create launcher
    if not args.test_only:
        print("🚀 Creating launcher...")
        create_launcher_script(gpu_info, recommended_model)
        print_usage_instructions()

if __name__ == "__main__":
    main()