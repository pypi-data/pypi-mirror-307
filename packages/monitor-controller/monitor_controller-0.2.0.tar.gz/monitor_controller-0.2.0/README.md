# Monitor Controller

Monitor Controller is a Python application that scans connected devices and monitors, and switches input sources based on the detected devices.

## Prerequisites

- Python 3.6+
- `pip` (Python package installer)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/monitor_controller.git
    cd monitor_controller
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the main program:
    ```sh
    python __main__.py
    ```

2. Follow the prompts to configure the application:
    - Select a trigger device from the list of connected devices.
    - The program will scan for connected monitors and configure the settings.

3. The program will start listening for events and switch monitor input sources based on the detected devices.

4. To exit the program, press `Enter` in the terminal.

## Configuration

The configuration is saved in a `config.json` file in the working directory. The file contains the selected trigger device and monitor settings.

## Logging

Logs are generated to help with debugging and monitoring the application's behavior. The logs include information about detected devices, monitor settings, and actions taken by the application.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.