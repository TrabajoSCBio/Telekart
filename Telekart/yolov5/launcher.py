# python detect.py --weights /runs/train/last.pt --img 640 --conf 0.25 --source mano2.jpg

from numpy import empty
import torch
import cv2
import socket

# Model
model = torch.hub.load('./', "custom",source = 'local' ,path="runs/train/custom/last" )

# Socket TCP/IP


vid = cv2.VideoCapture(0)
  
while(True):
    
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
  
    # Display the resulting frame
    results = model(frame)
    datos = results.pandas().xyxy[0]
    if not datos.empty:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Conexion con el puerto que esta escuchando
        server_address = ('localhost', 55001)
        print('connecting to {} port {}'.format(*server_address))
        sock.connect(server_address)

        gesto = datos["name"].to_numpy()
        gesto = gesto[0]
        x = datos["xmin"] + (datos["xmax"]-datos["xmin"])/2
        x = x.to_numpy()
        x = x[0]
        width = frame.shape[1]
        regionSize = width/3
        region = "desconocido"
        if x >= regionSize*2:
            region = "izquierda"
        elif x>= regionSize:
            region = "centro"
        else:
            region = "derecha"
        print(gesto)
        print(region)
        try:
        # Send data
            sock.sendall(gesto.encode())
            sock.sendall(region.encode())
            sock.close()

        except:
            sock.close()

    #cv2.imshow('frame', frame)

    #pulsar q para terminar el script
    if cv2.waitKey(1) & 0xFF == ord('q'):
        sock.close()
        break