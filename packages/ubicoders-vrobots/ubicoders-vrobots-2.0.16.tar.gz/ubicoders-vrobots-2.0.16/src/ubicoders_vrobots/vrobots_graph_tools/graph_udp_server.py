import asyncio
import time
import numpy as np


def parse_message(message):
    """Parse incoming message to extract X, Y, Z values."""
    try:
        timestamp, x, y, z = message.split(",")
        return np.array([float(timestamp), float(x), float(y), float(z)])
    except:
        return np.array([0.0, 0.0, 0.0, 0.0])


class UDPServerProtocol:
    def __init__(self, data_handler, port=12345, timeout=1):
        self.clients = {}
        self.timeout = timeout
        self.data_handler = data_handler
        self.port = port
        self.base_time = 0

    def connection_made(self, transport):
        self.transport = transport
        # print("Server started and waiting for messages...")
        asyncio.create_task(self.check_inactive_clients())

    def error_received(self, exc):
        print(f"Error received: {exc}")

    def datagram_received(self, data, addr):
        message = data.decode()
        data_point = parse_message(message)
        if len(self.clients) < 1:
            self.data_handler.clear_data()
            self.base_time = data_point[0]  # Set base_time to the first timestamp

        # Convert timestamp to relative time by subtracting base_time
        data_point[0] -= self.base_time
        self.clients[addr] = time.time()
        self.data_handler.append_data(data_point)

        # print(f"Message from {addr}: {message}")

    async def check_inactive_clients(self):
        while True:
            await asyncio.sleep(0.5)
            current_time = time.time()
            inactive_clients = [
                addr
                for addr, last_time in self.clients.items()
                if current_time - last_time > self.timeout
            ]
            for addr in inactive_clients:
                # print(f"Removing inactive client: {addr}")
                del self.clients[addr]


async def start_udp_server(data_handler, port=12345):
    loop = asyncio.get_running_loop()
    print(f"\033[92mUDP server running on {port}\033[0m")
    await loop.create_datagram_endpoint(
        lambda: UDPServerProtocol(data_handler, port), local_addr=("0.0.0.0", port)
    )
