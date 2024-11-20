import json
import zmq


# APP_ID = id here
UNITS = 'imperial'
DEGREES = 'fahrenheit'


# Create a zmq Context for creating sockets
context = zmq.Context()

# Print message before trying to connect
print("Client attempting to connect to server...")

# Create a request socket
socket = context.socket(zmq.REQ)
# Connect to tcp://localhost:5555
socket.connect("tcp://localhost:5555")

# If the user requests the service to stop set this to False
service_running = [True]
required_params = ['lat', 'lon']

def set_param(message):
    """
    Prompt the user with a message and set the given parameter.

    Args:
        message (str): The message to prompt the user with.
        param_name (str): The name of the parameter to get from the user.

    Returns:
        obj: The value of the param requested.
    """

    param_value = input(message)

    if param_value == 'STOP':
        service_running[0] = False

    return param_value

def get_params(params):
    """
    Get params to make a request.

    Args:
        params (list): The parameters to make a request.

    Returns:
        dict: The params requested and their values.
    """
    param_dict = {}
    for param in params:
        param_dict[param] = set_param(f"Enter a value for {param}")
        # Don't continue if user chose to stop.
        if param_dict[param] == 'STOP':
            service_running[0] = False
            return

    return param_dict


# The example program:
print(f"\nWelcome to example Weather app! Enter 'STOP' at anytime to stop the service.\n")

while service_running[0]:
    # Get the req type:
    req_type = set_param("Would like like to see the weather today, or the 5-day forecast? Enter" +
                        f" 'weather' to get the weather, or 'forecast' to get the forecast.\n")
    if req_type == 'STOP':
        break
    while req_type != 'weather' and req_type != 'forecast':
        req_type = set_param(f"Please type 'weather' or 'forecast'\n")

    # Get the required params
    params = get_params(required_params)
    if not service_running[0]:
        break
    params['units'] = UNITS

    # Send the request.
    request = {
        'req': req_type,
        'params': params,
        'appid': APP_ID
    }
    print(f"Sending a request -- {request}...")
    socket.send_json(request)
    # Get the reply
    message = socket.recv()
    message = message.decode()
    data = json.loads(message)
    # Print the message
    print(f"Server sent back: {message}")
    if req_type == 'weather':
        print(f"\n\nIt's {data['main']['temp']} degrees {DEGREES} out today.\n\n")

# Stop the server
socket.send_json({'req': 'STOP'})
message = socket.recv()
print(f"Server sent back: {message.decode()}")