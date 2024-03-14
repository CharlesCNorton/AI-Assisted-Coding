import serial
import pynmea2
import time


def print_menu(current_port, current_baudrate, continuous_mode):
    print("\nGPS Reader Menu:")
    print("1. Start reading GPS data")
    print(f"2. Set COM port (Current: {current_port})")
    print(f"3. Set baud rate (Current: {current_baudrate})")
    mode = "Continuous" if continuous_mode else "Single"
    print(f"4. Toggle GPS data report mode (Current: {mode})")
    print("5. Exit")


def get_gps_position(port='COM3', baudrate=9600, continuous=False):
    position_data = {
        "latitude": None, "longitude": None,
        "altitude": None, "speed": None, "time": None
    }

    try:
        with serial.Serial(port, baudrate=baudrate, timeout=1) as ser:
            mode = 'Streaming' if continuous else 'Fetching single'
            print(f"Connected to GPS on {port}. {mode} data...")
            while True:
                try:
                    line = ser.readline().decode('ascii', errors='replace')

                    if line.startswith(('$GNGGA', '$GPGGA')):
                        msg = pynmea2.parse(line)
                        if msg.gps_qual > 0:
                            position_data["latitude"] = f"{msg.latitude:.8f} {msg.lat_dir}"
                            position_data["longitude"] = f"{msg.longitude:.8f} {msg.lon_dir}"
                            altitude_meters = msg.altitude
                            position_data["altitude"] = f"{altitude_meters * 3.28084:.2f} ft"
                            position_data["time"] = msg.timestamp.strftime("%H:%M:%S")

                    if line.startswith(('$GNVTG', '$GPVTG')):
                        msg = pynmea2.parse(line)
                        speed_kph = msg.spd_over_grnd_kmph
                        speed_mph = speed_kph * 0.621371
                        position_data["speed"] = "0.00 mph" if speed_mph < 1 else f"{speed_mph:.2f} mph"

                    if all(value is not None for value in position_data.values()):
                        print("Time (UTC): {}, Latitude: {}, Longitude: {}, Altitude: {}, Speed: {}".format(
                            position_data['time'], position_data['latitude'],
                            position_data['longitude'], position_data['altitude'],
                            position_data['speed']
                        ))
                        if not continuous:
                            break
                        else:
                            position_data = {key: None for key in position_data.keys()}

                except pynmea2.ParseError:
                    print("Received malformed NMEA data, trying again...")

                if continuous:
                    time.sleep(0.10)
    except serial.SerialException as e:
        print(f"Error opening serial port {port}: {e}")
    except serial.SerialTimeoutException:
        print(f"Timeout error on serial port {port}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    port = 'COM3'
    baudrate = 9600
    continuous_mode = False

    while True:
        print_menu(port, baudrate, continuous_mode)
        choice = input("Select an option: ").strip()
        if choice == '1':
            get_gps_position(port, baudrate, continuous_mode)
        elif choice == '2':
            port = input("Enter new COM port (e.g., COM3): ").strip()
        elif choice == '3':
            baudrate_input = input("Enter new baud rate (e.g., 9600): ").strip()
            try:
                baudrate = int(baudrate_input)
            except ValueError:
                print("Invalid baud rate. Please enter a number.")
        elif choice == '4':
            continuous_mode = not continuous_mode
            print(f"GPS data report mode set to {'Continuous' if continuous_mode else 'Single'} report.")
        elif choice == '5':
            print("Exiting GPS Reader.")
            break
        else:
            print("Invalid choice. Please select a valid option.")
