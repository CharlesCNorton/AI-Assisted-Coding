import serial
import pynmea2
import time
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

plot_map = False
map_initialized = False
fig, ax = None, None  # Initialize figure and axes for plotting
m = None  # Initialize the Basemap instance
plot, = None,  # Initialize the plot

def print_menu(current_port, current_baudrate, continuous_mode, plot_map):
    print("\nGPS Reader Menu:")
    print("1. Start reading GPS data")
    print(f"2. Set COM port (Current: {current_port})")
    print(f"3. Set baud rate (Current: {current_baudrate})")
    mode = "Continuous" if continuous_mode else "Single"
    print(f"4. Toggle GPS data report mode (Current: {mode})")
    print(f"5. Toggle map visualization (Current: {'On' if plot_map else 'Off'})")
    print("6. Exit")

def initialize_map(latitude, longitude):
    global fig, ax, m, plot
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 6))
    m = Basemap(projection='cyl', llcrnrlat=latitude-5, urcrnrlat=latitude+5,
                llcrnrlon=longitude-5, urcrnrlon=longitude+5, resolution='i', ax=ax)
    m.drawmapboundary(fill_color='aqua')
    m.fillcontinents(color='coral', lake_color='aqua')
    m.drawcoastlines()
    x, y = m(longitude, latitude)
    plot, = m.plot(x, y, 'bo', markersize=12)
    plt.title('GPS Position')

def update_map(latitude, longitude):
    global plot, m
    x, y = m(longitude, latitude)
    plot.set_data(x, y)
    plt.draw()
    plt.pause(0.01)

def plot_on_map(latitude, longitude):
    global map_initialized
    if not map_initialized:
        initialize_map(latitude, longitude)
        map_initialized = True
    else:
        update_map(latitude, longitude)

def get_gps_position(port='COM3', baudrate=9600, continuous=False):
    global plot_map, map_initialized
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
                            latitude = msg.latitude
                            if msg.lat_dir == 'S':
                                latitude = -latitude
                            longitude = msg.longitude
                            if msg.lon_dir == 'W':
                                longitude = -longitude
                            position_data["latitude"] = latitude
                            position_data["longitude"] = longitude
                            altitude_meters = msg.altitude
                            position_data["altitude"] = f"{altitude_meters * 3.28084:.2f} ft"
                            position_data["time"] = msg.timestamp.strftime("%H:%M:%S")

                    if line.startswith(('$GNVTG', '$GPVTG')):
                        msg = pynmea2.parse(line)
                        speed_kph = msg.spd_over_grnd_kmph
                        speed_mph = speed_kph * 0.621371
                        position_data["speed"] = "0.00 mph" if speed_mph < 1 else f"{speed_mph:.2f} mph"

                    if all(value is not None for value in position_data.values()):

                        if position_data["longitude"] > 0:
                            position_data["longitude"] = -position_data["longitude"]

                        print("Time (UTC): {}, Latitude: {}, Longitude: {}, Altitude: {}, Speed: {}".format(
                            position_data['time'], position_data['latitude'],
                            position_data['longitude'], position_data['altitude'],
                            position_data['speed']
                        ))
                        if plot_map:
                            plot_on_map(position_data['latitude'], position_data['longitude'])
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
        print_menu(port, baudrate, continuous_mode, plot_map)
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
            plot_map = not plot_map
            if not plot_map and map_initialized:
                plt.close()
                map_initialized = False  # Ensure map is re-initialized next time plotting is enabled
            print(f"Map visualization set to {'On' if plot_map else 'Off'}.")
        elif choice == '6':
            print("Exiting GPS Reader.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

