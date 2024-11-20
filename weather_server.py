import zmq
import requests
import json


# Create a zmq Context for creating sockets
context = zmq.Context()
# Create a reply socket
socket = context.socket(zmq.REP)
# Bind the socket to tcp://*:5555
socket.bind("tcp://*:5555")


def get_weather_data(req, params, appid):
    query = ''
    for param in params:
        query += f"{param}={params[param]}&"
    url = f"https://api.openweathermap.org/data/2.5/{req}?{query}appid={appid}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            return 'Error: ', response.status_code

    except requests.exceptions.RequestException as e:
        return 'Error: ', e


# Infinite loop to wait to receive a message from the client
while True:

    # recv will receive a message from the client

    message = socket.recv()
    print(message)
    # Send a message back to the client if a message was received
    if len(message) > 0:
        # Decode the message to string -> convert to json -> convert to dict
        data = json.loads(message)
        # If client asked server to quit
        if data['req'] == 'STOP':
            socket.send_string('Service ended.')
            break
        req = data['req']
        params = data['params']
        appid = data['appid']

        # Send reply back to client
        socket.send_json(get_weather_data(req, params, appid))


# Close sockets
context.destroy()