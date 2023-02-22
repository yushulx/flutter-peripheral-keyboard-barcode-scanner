# Peripheral Keyboard and Barcode Scanner

The project demonstrates how to turn a Flutter mobile app into a peripheral keyboard and barcode scanner to input data into PCs.

## Setting Up the Python Server
1. Install [pyautogui](https://pypi.org/project/PyAutoGUI/), [websockets](https://pypi.org/project/websockets/) and [zeroconf](https://pypi.org/project/zeroconf/) using pip:
    ```bash
    pip install pyautogui
    ```
2. Change the port numbers for Bonjour service and web socket server if they are already in use.
    ```python
    # Bonjour
    info = ServiceInfo("_bonsoirdemo._tcp.local.",
                    "Python Web Socket Server._bonsoirdemo._tcp.local.",
                    port=7000, addresses=[ip_address])

    # Web Socket Server
    s = await websockets.serve(server, ip_address, 4000)
    ```

    If you change the web socket port in the server, you also need to change the port in the Flutter app.
    ```dart
    _connect('${widget.service.ip}:4000');
    ```

3. Run the server:
    ```bash
    python server.py
    ```