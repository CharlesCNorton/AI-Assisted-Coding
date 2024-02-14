
# EZRequirements

EZRequirements is a simple Python GUI application designed to manage Python package dependencies efficiently. It streamlines the process of updating and installing packages from a `requirements.txt` file, while also performing safety checks for known vulnerabilities using `pip-audit`.

## Features

- **Update/Install Packages**: Easily update or install packages specified in a `requirements.txt` file.
- **Package Safety Check**: Before installation, perform a safety check on packages for known vulnerabilities using `pip-audit`.
- **GUI Based**: User-friendly graphical interface to select a `requirements.txt` file and manage package installations.

## Installation

Before running EZRequirements, ensure you have Python and `pip` installed on your system. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.6+
- `pip-audit` for performing safety checks on packages.

## Usage

1. Start the application by running `python ezrequirements.py` in your terminal.
2. Click on "Select requirements.txt and Update/Install Packages" to choose your `requirements.txt` file.
3. The application will first perform a safety check using `pip-audit` and then proceed to update/install the packages.

## Contributing

Contributions to EZRequirements are welcome! Feel free to fork the repository, make changes, and submit pull requests.

## License

EZRequirements is released under the MIT License. See the LICENSE file for more details.
