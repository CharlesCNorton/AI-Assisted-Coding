
import subprocess
import os
import re
import threading
from tkinter import Tk, Label, Button, filedialog, messagebox, Toplevel, Scrollbar, Text, VERTICAL, END

def run_shell_command(command):
    """Execute a shell command and return the success status and output."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def perform_package_safety_check(requirements_path):
    """Perform a safety check on packages listed in the requirements.txt file using pip-audit."""
    success, output = run_shell_command(f"pip-audit -r {requirements_path} --json")
    if success and output.strip():
        vulnerabilities = output
        messagebox.showinfo("Safety Check", "Some packages may have known vulnerabilities. Check the console for details.")
        print(vulnerabilities)
    elif success:
        messagebox.showinfo("Safety Check", "No known vulnerabilities found.")
    else:
        messagebox.showerror("Safety Check Error", "Failed to perform safety check. Check console for details.")
        print(output)

def update_install_versions(specified_versions):
    """Update or install the specified package versions in a background thread."""
    results = "Starting package updates/installations...\n"
    for package, version in specified_versions.items():
        pkg_install = f"{package}{version}" if version else package
        command = f"{sys.executable} -m pip install {pkg_install}"
        success, output = run_shell_command(command)
        if success:
            results += f"Successfully processed {pkg_install}\n"
        else:
            results += f"Failed to process {pkg_install}: {output}\n"
    show_results_window(results)

def show_results_window(results):
    """Display the results of package updates/installations in a new window."""
    window = Toplevel(root)
    window.title("Results")
    text_area = Text(window, wrap="word")
    text_area.pack(expand=True, fill="both")
    scrollbar = Scrollbar(window, command=text_area.yview, orient=VERTICAL)
    scrollbar.pack(side="right", fill="y")
    text_area['yscrollcommand'] = scrollbar.set
    text_area.insert(END, results)
    text_area.config(state="disabled")

def handle_update_install():
    """Handle the button click for updating/installing packages."""
    file_path = select_file_or_folder()
    if file_path:
        specified_versions = read_requirements_file(file_path)
        # Perform safety check before proceeding with installations
        perform_package_safety_check(file_path)
        threading.Thread(target=lambda: update_install_versions(specified_versions), daemon=True).start()

def select_file_or_folder():
    """Prompt the user to select a requirements.txt file."""
    file_path = filedialog.askopenfilename(title="Select requirements.txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not file_path:
        messagebox.showwarning("Warning", "No file was selected.")
        return None
    return file_path

def read_requirements_file(file_path):
    """Parse the requirements.txt file and return a dictionary of packages and their version specifications."""
    specified_versions = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                continue  # Skip comments and empty lines
            match = re.match(r'([a-zA-Z0-9_-]+)([<>=!~]+.*)?', line)
            if match:
                pkg, ver_spec = match.groups()
                specified_versions[pkg] = ver_spec if ver_spec else None
            else:
                print(f"Unable to parse line: {line}")
    return specified_versions

if __name__ == "__main__":
    root = Tk()
    Label(root, text="Python Package Manager", font=("Helvetica", 16), pady=20).pack()
    Button(root, text="Select requirements.txt and Update/Install Packages", command=handle_update_install, padx=10, pady=5).pack()
    Button(root, text="Exit", command=root.destroy, padx=10, pady=5).pack()
    root.mainloop()
