import socket, time

def internet(host="8.8.8.8", port=53, timeout=3):
  """
  Host: 8.8.8.8 (google-public-dns-a.google.com)
  OpenPort: 53/tcp
  Service: domain (DNS/TCP)
  """
  try:
    socket.setdefaulttimeout(timeout)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    current_time = time.asctime()
    print("{} Online".format(current_time))

    with open("status.txt", mode="a") as f:
        f.write("{} Online\n".format(current_time))

  except socket.error as ex:
    current_time = time.asctime()
    print("{} Offline".format(current_time))

    with open("status.txt", mode="a") as f:
        f.write("{} Offline\n".format(current_time))

if __name__ == "__main__":
    while(True):
        internet()
        time.sleep(30)
