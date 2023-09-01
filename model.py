class IPAddress:
    def is_valid(cls, ip_address):
        pass
        
    def __init__(self, ip_address = 0, 
                 subnet_mask_length: int = 0):  # not needed if ip_address is str in CIDR notation with subnet mask length
        # default values
        self.ip_address: int = 0  # 32-bit integer
        self.subnet_mask_length: int = subnet_mask_length  # 0-32
        
        # case 1: argument is int
        if type(ip_address) is int:
            self.ip_address = ip_address
            
        # case 2: argument is str
        elif type(ip_address) is str:
            if "/" in ip_address:
                ip_address, subnet_mask_length_str = ip_address.split("/")
                self.subnet_mask_length = int(subnet_mask_length_str)
            if "." in ip_address:
                for i in ip_address.split('.'):
                    self.ip_address = self.ip_address * 256 + int(i)
            else:  # assume in binary form
                self.ip_address = int(ip_address, 2)
                
        # case 3: argument is IPAdress
        elif type(ip_address) is IPAddress:
            self.ip_address = ip_address.ip_address
            self.subnet_mask_length = ip_address.subnet_mask_length
            
        # case 4: argument is of invalid type
        else:
            raise Exception("Invalid argument type")
    
    def __repr__(self):
        str_digits = []
        for i in range(4):
            str_digits.append(str(self.ip_address % 256))
            self.ip_address //= 256
        return '.'.join(str_digits[::-1]) + '/' + str(self.subnet_mask_length)

class IPAddressBlock:
    def __init__(self, network_ip_address):
        self.network_ip_address = network_ip_address

class Organization:
    def __init__(self, name, ip_addresses=None):
        self.name = name
        self.ip_addresses = ip_addresses if ip_addresses is not None else []
    
class Database:
    def __init__(self):
        self.organizations = []
        