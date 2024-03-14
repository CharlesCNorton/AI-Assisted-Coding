# PyNavGPS

PyNavGPS is a Python-based utility for reading and interpreting GPS data from serially connected GPS modules. Designed to be simple yet powerful, PyNavGPS offers both continuous and single-fetch modes, making it ideal for various applications ranging from hobbyist projects to more advanced geolocation solutions.

## Features

- Read GPS data through serial connections.
- Supports both continuous and single data fetch modes.
- Displays key GPS information: latitude, longitude, altitude, speed, and timestamp.
- Easy to use command-line interface.
- Customizable COM port and baud rate settings.

## Installation

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/yourusername/PyNavGPS.git
   ```
2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To start PyNavGPS, navigate to the cloned repository directory and run:

```
python pynavgps.py
```

Follow the on-screen menu to select your desired operation mode and settings.

## Dependencies

- Python 3.6 or higher
- pySerial
- pynmea2

These can be installed using the `pip install -r requirements.txt` command.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- Thanks to the Python community for the extensive libraries and support.
