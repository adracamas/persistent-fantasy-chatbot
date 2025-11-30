#!/usr/bin/env python3
"""
Standalone Installer for Fantasy Chatbot
Creates a completely self-contained environment without Pinokio
"""

import os
import sys
import subprocess
import platform
import urllib.request
from pathlib import Path

def run_command(command, description):
    """Run a shell command with error handling."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_python():
    """Check Python version."""
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print("✅ Python version OK")
    return True

def create_venv():
    """Create virtual environment."""
    venv_path = Path("fantasy_env")
    
    if venv_path.exists():
        print("⚠️  Virtual environment already exists")
        response = input("Remove and recreate? (y/N): ")
        if response.lower() == 'y':
            import shutil
            shutil.rmtree(venv_path)
        else:
            print("Using existing environment")
            return True
    
    print("📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "fantasy_env"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False

def get_pip_command():
    """Get pip command for the virtual environment."""
    if platform.system() == "Windows":
        return "fantasy_env\\Scripts\\pip.exe"
    else:
        return "fantasy_env/bin/pip"

def install_dependencies():
    """Install all dependencies."""
    pip_cmd = get_pip_command()
    
    commands = [
        (f"{pip_cmd} install --upgrade pip", "Upgrading pip"),
        (f"{pip_cmd} install -r requirements.txt", "Installing dependencies"),
        (f"{pip_cmd} list", "Verifying installation"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def verify_installation():
    """Verify all components are installed."""
    pip_cmd = get_pip_command()
    
    test_commands = [
        (f"{pip_cmd} exec python -c 'import torch; print(f\"PyTorch: {torch.__version__}\")'", "Testing PyTorch"),
        (f"{pip_cmd} exec python -c 'import transformers; print(\"Transformers OK\")'", "Testing Transformers"),
        (f"{pip_cmd} exec python -c 'import sentence_transformers; print(\"Sentence Transformers OK\")'", "Testing Sentence Transformers"),
    ]
    
    print("\n🔍 Verifying installation...")
    all_ok = True
    for command, description in test_commands:
        if not run_command(command, description):
            all_ok = False
    
    return all_ok

def create_launcher():
    """Create launcher scripts."""
    system = platform.system()
    
    if system == "Windows":
        # Windows batch file
        bat_content = '''@echo off
echo Starting Fantasy Chatbot...
call fantasy_env\\Scripts\\activate.bat
python fantasy_chatbot.py
pause
'''
        with open("launch_fantasy_chatbot.bat", "w") as f:
            f.write(bat_content)
        
        # Web launcher
        web_bat_content = '''@echo off
echo Starting Fantasy Chatbot Web Interface...
call fantasy_env\\Scripts\\activate.bat
python web_interface.py
pause
'''
        with open("launch_web_interface.bat", "w") as f:
            f.write(web_bat_content)
            
        print("✅ Created Windows launcher scripts")
        
    else:
        # Unix shell script
        sh_content = '''#!/bin/bash
echo "Starting Fantasy Chatbot..."
source fantasy_env/bin/activate
python fantasy_chatbot.py
'''
        with open("launch_fantasy_chatbot.sh", "w") as f:
            f.write(sh_content)
        
        # Make executable
        os.chmod("launch_fantasy_chatbot.sh", 0o755)
        
        # Web launcher
        web_sh_content = '''#!/bin/bash
echo "Starting Fantasy Chatbot Web Interface..."
source fantasy_env/bin/activate
python web_interface.py
'''
        with open("launch_web_interface.sh", "w") as f:
            f.write(web_sh_content)
        
        os.chmod("launch_web_interface.sh", 0o755)
        
        print("✅ Created Unix launcher scripts")

def download_models():
    """Download initial models."""
    pip_cmd = get_pip_command()
    
    print("\n📥 Downloading AI models (this may take several GB)...")
    print("Models will be cached for faster loading")
    
    # Test model download
    test_command = f'{pip_cmd} exec python -c "from transformers import AutoModel; AutoModel.from_pretrained(\\"microsoft/DialoGPT-medium\\")"'
    
    try:
        subprocess.run(test_command, shell=True, check=True, timeout=300)
        print("✅ Model download completed")
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        print("⚠️  Model download failed or timed out")
        print("   Models will be downloaded on first use")
        return False

def main():
    """Main installation process."""
    print("🏰 Fantasy Chatbot - Standalone Installer")
    print("=" * 50)
    
    steps = [
        ("Checking Python", check_python),
        ("Creating virtual environment", create_venv),
        ("Installing dependencies", install_dependencies),
        ("Verifying installation", verify_installation),
        ("Creating launchers", create_launcher),
        ("Downloading models", download_models),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"\n❌ Installation failed at: {step_name}")
            print("Please check the error messages above and try again.")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Installation completed successfully!")
    print("\n🚀 Launch the chatbot:")
    
    system = platform.system()
    if system == "Windows":
        print("   • CLI: double-click 'launch_fantasy_chatbot.bat'")
        print("   • Web: double-click 'launch_web_interface.bat'")
        print("   • Manual: fantasy_env\\Scripts\\python.exe fantasy_chatbot.py")
    else:
        print("   • CLI: ./launch_fantasy_chatbot.sh")
        print("   • Web: ./launch_web_interface.sh")
        print("   • Manual: source fantasy_env/bin/activate && python fantasy_chatbot.py")
    
    print("\n📱 Web interface will be available at: http://localhost:8000")
    print("\n🧠 Your fantasy world memory will be saved in: fantasy_world.db")
    print("\n📖 See README.md for detailed usage instructions")
    print("\nEnjoy your persistent fantasy adventure! 🏰✨")

if __name__ == "__main__":
    main()