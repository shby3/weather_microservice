import zmq

APP_ID = '42bbc13b105bb92ea654f5abcbadc895'


# Create a zmq Context for creating sockets
context = zmq.Context()

# Print message before trying to connect
print("Client attempting to connect to server...")

# Create a request socket
socket = context.socket(zmq.REQ)
# Connect to tcp://localhost:5555
socket.connect("tcp://localhost:5555")

# Request a message from the server
print(f"Sending a request...")

# Send the user specified data. https://openweathermap.org/price#weather go to highlighted links under free
# for information on API calls.
request_1 = {
    'req': 'weather',
    'params': {'lat': 42.3601, 'lon': 71.0589},
    'appid': APP_ID
}
request_2 = {
    'req': 'forecast',
    'params': {'lat': 51.5072, 'lon': 0.1276, 'units': 'metric'},
    'appid': APP_ID
}
request_3 = {'req': 'STOP'}
requests = [request_1, request_2, request_3]

for request in requests:
    socket.send_json(request)
    # Get the reply
    message = socket.recv()
    # Print the message
    print(f"Server sent back: {message.decode()}")