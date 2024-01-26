import sys
import subprocess
from colorama import Fore, Style, init
from prettytable import PrettyTable
import torch
import torch.nn as nn

init(autoreset=True)

def print_header(message):
    print(Fore.BLUE + message + Style.RESET_ALL)

def print_info(message):
    print(Fore.YELLOW + message + Style.RESET_ALL)

def print_success(message):
    print(Fore.GREEN + message + Style.RESET_ALL)

def print_error(message):
    print(Fore.RED + message + Style.RESET_ALL)

def check_python_version():
    print_header("\n[Python Version]")
    print_info(f"Python Version: {sys.version}")

def check_system_path():
    print_header("\n[System PATH]")
    system_path = subprocess.check_output("echo %PATH%", shell=True).decode()
    print_info(system_path.strip())

def check_cuda_version():
    print_header("\n[CUDA Version]")
    try:
        cuda_version = subprocess.check_output("nvidia-smi", shell=True).decode()
        print_info(cuda_version)
    except subprocess.CalledProcessError:
        print_error("Failed to determine CUDA version. Make sure NVIDIA drivers are installed and 'nvidia-smi' is in your system's PATH.")

def check_cuda_path():
    try:
        cuda_path = subprocess.check_output("echo %CUDA_PATH%", shell=True).decode().strip()
        if cuda_path:
            print_header("\n[CUDA PATH]")
            print_info(cuda_path)
    except subprocess.CalledProcessError:
        print_error("CUDA PATH not set.")

def check_installed_packages():
    print_header("\n[Checking Installed Packages with Pip]")
    relevant_packages = ["torch", "torchaudio", "torchvision", "numpy", "tensorflow"]
    pip_command = f"{sys.executable} -m pip list"
    installed_packages = subprocess.check_output(pip_command, shell=True).decode()

    package_table = PrettyTable()
    package_table.field_names = ["Package", "Version"]
    for line in installed_packages.split('\n'):
        if any(pkg in line for pkg in relevant_packages):
            parts = line.split()
            if len(parts) >= 2:
                package_table.add_row(parts[:2])

    print_info(package_table.get_string())

def check_pytorch_installation():
    print_header("\n[PyTorch Information]")
    try:
        print_info(f"PyTorch Version: {torch.__version__}")
        print_info(f"PyTorch CUDA Support: {'Yes' if torch.version.cuda is not None else 'No'}")
        print_info(f"CUDA Available: {torch.cuda.is_available()}")
    except ImportError:
        print_error("PyTorch is not installed.")

def check_cuda_operations():
    print_header("\n[CUDA Operations Test]")
    gpu_count = torch.cuda.device_count()

    for i in range(gpu_count):
        print_header(f"Testing GPU {i} - {torch.cuda.get_device_name(i)}")
        print_info(f"Memory Allocated: {torch.cuda.memory_allocated(i)} bytes")
        print_info(f"Memory Cached: {torch.cuda.memory_reserved(i)} bytes")

        try:
            x = torch.tensor([1.0, 2.0, 3.0], device=f'cuda:{i}')
            y = torch.tensor([1.0, 2.0, 3.0], device=f'cuda:{i}')
            z = x + y
            print_success(f"Operation Result: {z}")
            print_success("SUCCESS: Simple tensor operation on GPU successful.")

            model = nn.Sequential(nn.Linear(10, 5), nn.ReLU(), nn.Linear(5, 2)).to(f'cuda:{i}')
            test_input = torch.randn(1, 10).to(f'cuda:{i}')
            output = model(test_input)
            print_success(f"Model Output: {output}")
            print_success("SUCCESS: Neural network model test successful.")
        except Exception as e:
            print_error(f"ERROR: {e}")

def show_menu():
    print_header("\nTorchCheck - PyTorch and CUDA Diagnostic Tool")
    print_info("1. Check Python Version")
    print_info("2. Check System PATH")
    print_info("3. Check CUDA Information")
    print_info("4. Check Installed Packages")
    print_info("5. Check PyTorch Installation")
    print_info("6. Check CUDA Operations")
    print_info("7. Run All Tests")
    print_info("0. Exit")
    print("\nEnter the number of the test you want to run:")

def run_diagnostics():
    while True:
        show_menu()
        choice = input()

        if choice == "1":
            check_python_version()
        elif choice == "2":
            check_system_path()
        elif choice == "3":
            check_cuda_version()
            check_cuda_path()
        elif choice == "4":
            check_installed_packages()
        elif choice == "5":
            check_pytorch_installation()
        elif choice == "6":
            check_cuda_operations()
        elif choice == "7":
            check_python_version()
            check_system_path()
            check_cuda_version()
            check_cuda_path()
            check_installed_packages()
            check_pytorch_installation()
            check_cuda_operations()
        elif choice == "0":
            break
        else:
            print_error("Invalid selection. Please try again.")

        print("\nPress Enter to continue...")
        input()

if __name__ == "__main__":
    run_diagnostics()
