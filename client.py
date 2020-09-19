import socket
import tqdm
import os
import sys
import tqdm

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 
def main():
	filename = sys.argv[1:][0]
	host = sys.argv[1:][1]
	port = int(sys.argv[1:][2])

	if os.path.exists(filename) == False: #if sending file not exist
		print("File not exist")
		return
		
	filesize = os.path.getsize(filename)
	s = socket.socket()

	print(f"[+] Connecting to {host}:{port}")
	s.connect((host, port))
	print("[+] Connected.\n",end='\n')

	print("[+] Sending file '"+filename+"'")

	s.send(f"{filename}{SEPARATOR}{filesize}".encode())
	progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
	with open(filename, "rb") as f:
		for _ in progress:
			bytes_read = f.read(BUFFER_SIZE)
			if not bytes_read:
				break
			s.sendall(bytes_read)
			progress.update(len(bytes_read))

	print("[+] Sent.\n")        
	print(f"[+] Disconnecting from {host}:{port}")
	s.close()
	print("[+] Disconnected.")

if __name__ == "__main__":
    main()


