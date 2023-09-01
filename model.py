class IPAddress:
    def __init__(self, ip_address = 0, 
                 subnet_mask_length: int = 0):  # not needed if ip_address is str in CIDR notation with subnet mask length
        # default values
        self.ip_address: int = 0  # 32-bit integer
        self.subnet_mask_length: int = subnet_mask_length  # 0-32
        
        # case 1: argument is int
        if isinstance(ip_address, int):
            self.ip_address = ip_address
            
        # case 2: argument is str
        elif isinstance(ip_address, str):
            if "/" in ip_address:
                ip_address, subnet_mask_length_str = ip_address.split("/")
                self.subnet_mask_length = int(subnet_mask_length_str)
            if "." in ip_address:
                for i in ip_address.split('.'):
                    if len(i) == 8:  # assume in binary form
                        self.ip_address = self.ip_address * 256 + int(i, 2)
                    else:  # if decimal
                        self.ip_address = self.ip_address * 256 + int(i)
            else:  # assume in binary form
                self.ip_address = int(ip_address, 2)
                
        # case 3: argument is IPAdress
        elif isinstance(ip_address, IPAddress):
            self.ip_address = ip_address.ip_address
            self.subnet_mask_length = ip_address.subnet_mask_length
            
        # case 4: argument is of invalid type
        else:
            raise Exception("Invalid argument type")
        
    def get_subnet_mask(self):
        return IPAddress(2 ** 32 - 2 ** (32 - self.subnet_mask_length))
    
    def __repr__(self):
        str_digits = []
        ip_address = self.ip_address
        for i in range(4):
            str_digits.append(str(ip_address % 256))
            ip_address //= 256
        return '.'.join(str_digits[::-1]) + ('/' + str(self.subnet_mask_length) if self.subnet_mask_length != 0 else '')

    def __eq__(self, other):
        return self.ip_address == other.ip_address and self.subnet_mask_length == other.subnet_mask_length
    
    def __lt__(self, other):
        return self.ip_address < other.ip_address
    
    def __gt__(self, other):
        return self.ip_address > other.ip_address
    
    def __le__(self, other):
        return self.ip_address <= other.ip_address
    
    def __ge__(self, other):
        return self.ip_address >= other.ip_address
    
    def __add__(self, other):
        if isinstance(other, int):
            return IPAddress(self.ip_address + other, self.subnet_mask_length)
        return IPAddress(self.ip_address + other.ip_address)
    
    def __sub__(self, other):
        if isinstance(other, int):
            return IPAddress(self.ip_address - other, self.subnet_mask_length)
        return IPAddress(self.ip_address - other.ip_address)
    
    def __iadd__(self, other):
        if isinstance(other, int):
            self.ip_address += other
        else:
            self.ip_address += other.ip_address
        return self
    
    def __isub__(self, other):
        if isinstance(other, int):
            self.ip_address -= other
        else:
            self.ip_address -= other.ip_address
        return self
    
    # deep copy
    def copy(self):
        return IPAddress(self.ip_address, self.subnet_mask_length)

class IPAddressBlock:
    def __init__(self, network_ip_address: IPAddress):
        self.ip_address: IPAddress = network_ip_address
        
    def get_identity_address(self):
        return self.ip_address.copy()

    def get_broadcast_address(self):
        return self.ip_address + self.num_usable_addresses()
    
    def lower_bound_address(self):
        return self.ip_address + 1
    
    def upper_bound_address(self):
        return self.ip_address + self.num_usable_addresses() - 1
    
    def num_usable_addresses(self):
        return 2 ** (32 - self.ip_address.subnet_mask_length)
    

class Organization:
    def __init__(self, name, ip_addresses=None):
        self.name = name
        self.ip_addresses = ip_addresses if ip_addresses is not None else []
    
class Database:
    def __init__(self):
        self.organizations = []
        