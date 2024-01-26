TorchCheck - PyTorch and CUDA Diagnostic Tool
---------------------------------------------

Description:
TorchCheck is a Python-based diagnostic tool designed to check and report the status of your PyTorch installation, CUDA compatibility, and system environment related to deep learning workflows.

Requirements:
- Python 3.8 or higher
- PyTorch
- prettytable
- colorama
- NVIDIA GPU with CUDA (for CUDA related tests)

Installation:
1. Ensure Python 3.8 or higher is installed on your system.
2. Install PyTorch following the official guide at https://pytorch.org/get-started/locally/
3. Install additional required packages:
   pip install prettytable colorama

Usage:
1. Run the script in a Python environment.
2. A menu will be displayed with various options for diagnostics:
   - Check Python Version
   - Check System PATH
   - Check CUDA Information
   - Check Installed Packages
   - Check PyTorch Installation
   - Check CUDA Operations
   - Run All Tests
   - Exit
3. Choose an option by entering the corresponding number and pressing Enter.
4. View the diagnostic results.
5. Press Enter to return to the main menu after viewing the results of a test.
6. To exit the tool, choose the 'Exit' option.

Features:
- Check the Python version to ensure compatibility with PyTorch.
- Verify the System PATH for necessary dependencies.
- Display CUDA version and CUDA PATH to validate CUDA installation.
- List installed Python packages relevant to PyTorch and deep learning.
- Validate the PyTorch installation, including CUDA support.
- Perform operations testing on the GPU to ensure proper functioning of CUDA with PyTorch.
- Interactive menu for user-friendly navigation through various diagnostic checks.

Note:
This tool is intended for diagnostic purposes and assumes a basic understanding of Python, PyTorch, and CUDA environments. If you encounter any issues with your PyTorch or CUDA setup, refer to the official documentation or seek assistance from relevant online communities.

Author: [Your Name]
Version: 1.0
License: [Appropriate License]
