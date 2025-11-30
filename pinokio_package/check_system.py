# System Requirements Check
# This script verifies all system dependencies are available

import subprocess
import sys
import platform
import os

def check_command_exists(command):
    """Check if a command exists in PATH."""
    try:
        subprocess.run([command, '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_python():
    """Check Python installation."""
    print(f"Python: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print("✅ Python version OK")
        return True

def check_pip():
    """Check pip installation."""
    if check_command_exists("pip"):
        print("✅ pip available")
        return True
    else:
        print("❌ pip not found")
        return False

def check_gpu_drivers():
    """Check NVIDIA GPU drivers."""
    if check_command_exists("nvidia-smi"):
        try:
            result = subprocess.run(["nvidia-smi"], capture_output=True, text=True, check=True)
            print("✅ NVIDIA drivers found")
            print(f"Driver info: {result.stdout.split('Driver Version')[1].split('CUDA')[0].strip()}")
            return True
        except:
            print("❌ NVIDIA drivers found but nvidia-smi failed")
            return False
    else:
        print("❌ NVIDIA drivers not found")
        print("   Install from: https://www.nvidia.com/drivers")
        return False

def check_cuda():
    """Check CUDA installation."""
    try:
        import torch
        if torch.cuda.is_available():
            cuda_version = torch.version.cuda
            print(f"✅ CUDA {cuda_version} available")
            gpu_count = torch.cuda.device_count()
            for i in range(gpu_count):
                gpu_name = torch.cuda.get_device_name(i)
                memory = torch.cuda.get_device_properties(i).total_memory / 1e9
                print(f"   GPU {i}: {gpu_name} ({memory:.1f}GB)")
            return True
        else:
            print("❌ CUDA not available")
            return False
    except ImportError:
        print("❌ PyTorch not installed")
        return False

def main():
    print("🔍 System Requirements Check")
    print("=" * 40)
    
    checks = [
        ("Python", check_python),
        ("pip", check_pip),
        ("GPU Drivers", check_gpu_drivers),
        ("CUDA", check_cuda),
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n{name}:")
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            print(f"❌ Check failed: {e}")
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✅ All system requirements satisfied!")
        print("🚀 Ready to run Fantasy Chatbot")
    else:
        print("❌ Some requirements missing")
        print("📋 Please install missing dependencies")
        sys.exit(1)

if __name__ == "__main__":
    main()