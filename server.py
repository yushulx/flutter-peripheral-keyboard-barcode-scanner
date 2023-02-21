import asyncio
import websockets
import socket
import pyautogui
import signal

from zeroconf import ServiceBrowser, ServiceInfo, ServiceListener, Zeroconf
import socket

connected = set()
isShutdown = False

class MyListener(ServiceListener):

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        print(f"Service {name} added, service info: {info}")


async def handle_message(websocket, path):
    async for message in websocket:
        if isinstance(message, str):
            if message != '':
                # Handle a text message
                print(f'Received text message: {message}')
                if message == 'backspace':
                    pyautogui.press('backspace')
                elif message == 'enter':
                    pyautogui.press('enter')
                else:
                    pyautogui.typewrite(message)
                await websocket.send(message)
                
        elif isinstance(message, bytes):
            pass            
            

async def server(websocket, path):
    # Add the new client's websocket to the set of connected clients
    connected.add(websocket)
    try:
        # Start handling incoming messages from the client
        await handle_message(websocket, path)
    except:
        connected.remove(websocket)
      

def ctrl_c(signum, frame):
    global isShutdown
    isShutdown = True
    
async def main(ip_address):
    global isShutdown
    # Start the server
    s = await websockets.serve(server, ip_address, 7000)

    while not isShutdown:
        await asyncio.sleep(1)
        
    print("Shutting down server")
    s.close()
    await s.wait_closed()

if __name__ == '__main__':
    ip_address_str = "192.168.8.72"
    # Convert the IP address string to a binary representation
    ip_address = socket.inet_aton(ip_address_str)

    info = ServiceInfo("_bonsoirdemo._tcp.local.",
                    "Python Web Socket Server._bonsoirdemo._tcp.local.",
                    port=4000, addresses=[ip_address])

    zeroconf = Zeroconf()
    # Register the Bonjour service
    zeroconf.register_service(info)
    listener = MyListener()
    browser = ServiceBrowser(zeroconf, "_bonsoirdemo._tcp.local.", listener)
    
    # Start the web socket server
    signal.signal(signal.SIGINT, ctrl_c)
    asyncio.run(main(ip_address_str))

    # Unregister the Bonjour service
    print("Unregistering Bonjour service")
    zeroconf.unregister_service(info)
    zeroconf.close()