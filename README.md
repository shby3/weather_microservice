# weather_microservice

Import json and zmq in your program to REQUEST and RECEIVE data.

How to programmatically REQUEST data: 
  1. Create a request socket and connect to tcp://localhost:5555
  2. Send a python dict as a json to the socket. The dict should be as follows: {'req': request type, 'params': parameters (except for appid), 'appid': The API key to use} 'req' can be 'weather', 'forecast', or 'STOP' (if it's stop, the dict can just be {'req': 'STOP'}. Visit https://openweathermap.org/current and https://openweathermap.org/forecast5 for information on making the 'weather' or 'forecast' call.
Example:
  context = zmq.Context()
  socket = context.socket(zmq.REQ)
  socket.connect("tcp://localhost:5555")
  socket.send_json({'req': 'forecast', 'params': {'lat': 51.5072, 'lon': 0.1276, 'units': 'metric'}, 'appid': APP_ID})

How to programmatically RECEIVE data:
  1. Get the reply message from the server and decode it.
  2. The message is decoded as a string. Convert it to a dict to work with the data.
Example:
  message = socket.recv()
  message = message.decode()
  data = json.loads(message)
  if req_type == 'weather':
     print(f"\n\nIt's {data['main']['temp']} degrees out today.\n\n")
