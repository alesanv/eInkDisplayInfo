import socket


class DeviceNetworkDetails:

    def __init__(self):
        self.hostname=socket.gethostname()
        self.ip_addr = self._get_ip_address()
        

    #Get local IP address
    def getIpAddress(self):
        return self.ip_addr

    #Get hostname
    def getHostname(self):
        return self.hostname

    #Get the IP address from the Raspberry Pi
    def _get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1)) #connect() for UDP doesn't send packets
            ip_addr = s.getsockname()[0]
        except:
            ip_addr = "ERROR"
            print("Error retrieving network details")
        finally:
            s.close()
        return ip_addr
