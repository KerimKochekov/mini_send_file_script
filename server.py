import socket
import os
import tqdm

SERVER_HOST = "0.0.0.0"  # ip address
SERVER_PORT = 8800  # port number
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
while True:

    client_socket, address = s.accept()
    print(f"[+] {address} is connected.")

    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filesize = int(filesize)
    filename = os.path.basename(filename)

    # if file already exist
    if(os.path.exists(filename) == True):
        ind, ext = 0, filename.rfind(".")  # exclude extension format of file
        # search new name by adding some integer to the end of file name
        while(os.path.exists(filename[:ext] + str(ind) + filename[ext:]) == True):
            ind = ind + 1
        filename = filename[:ext] + str(ind) + filename[ext:]

    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        
    with open(filename, "wb") as f:
        for _ in progress:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
        progress.update(len(bytes_read))

    print("	[+] FIle named '" + filename + "' successfully downloaded.")
    client_socket.close()
    print(f"[+] {address} is disconnected.\n", end="\n")

s.close()
