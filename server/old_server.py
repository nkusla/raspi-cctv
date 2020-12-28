import socket
import picamera

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '192.168.0.19'
port = 80

camera = picamera.PiCamera()
camera.rotation = 180

server_socket.bind((host, port))
server_socket.listen(5)

while True:
    client_socket, address = server_socket.accept()
    camera.capture('capture.jpg', resize=(640, 480))

    print('Server succesfully connected to ' + str(address))
    
    request = client_socket.recv(1024).decode('utf-8')
    request = request.split(' ')[1]

    print('Client request ', request)

    requesting_file = request.split('?')[0]
    requesting_file = requesting_file.lstrip('/')
    if(requesting_file == ''):
        requesting_file = 'index.html'

    header = 'HTTP/1.1 200 OK\n'

    if(requesting_file.endswith('.jpg')):
        file_type = 'image/jpg'
    else:
        file_type = 'text/html'

    header += 'Content-Type: ' + file_type + '\n\n'
    contents = ''
    try:
        with open(requesting_file, 'rb') as f:
            contents = f.read()
        
        data = header.encode('UTF-8') + contents
        client_socket.send(data)
    except:
        pass

    client_socket.close()