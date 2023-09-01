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
        
    def get_subnet_mask(self) -> 'IPAddress':
        return IPAddress(2 ** 32 - 2 ** (32 - self.subnet_mask_length))
    
    # deep copy
    def get_copy(self) -> 'IPAddress':
        return IPAddress(self.ip_address, self.subnet_mask_length)
    
    def get_network_address(self) -> 'IPAddress':
        return IPAddress(self.ip_address & self.get_subnet_mask().ip_address)
    
    def get_host_address(self) -> 'IPAddress':
        return IPAddress(self.ip_address & ~self.get_subnet_mask().ip_address)
    
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

class IPAddressBlock:
    def __init__(self, network_ip_address: IPAddress):
        self.ip_address: IPAddress = network_ip_address
        
    def get_identity_address(self) -> 'IPAddress':
        return self.ip_address.get_copy()

    def get_broadcast_address(self) -> 'IPAddress':
        return self.ip_address + self.get_num_usable_addresses() - 1
    
    def get_lower_bound_address(self) -> 'IPAddress':
        return self.ip_address + 1
    
    def get_upper_bound_address(self) -> 'IPAddress':
        return self.ip_address + self.get_num_usable_addresses() - 2
    
    def get_num_usable_addresses(self) -> int:
        return 2 ** (32 - self.ip_address.subnet_mask_length)
    
    def contains(self, ip_address: IPAddress) -> bool:  # checks if an ip address is in the block, including identity and broadcast addresses
        return self.get_identity_address() <= ip_address <= self.get_broadcast_address()
    
    def __iter__(self):  # iterates through all addresses in the block except the network and broadcast addresses
        self.current_address = self.get_lower_bound_address()
        self.get_upper_bound_address = self.get_upper_bound_address()
        return self
    
    def __next__(self):
        if self.current_address > self.get_upper_bound_address:
            raise StopIteration
        else:
            self.current_address += 1
            return self.current_address - 1
    
    def __repr__(self):
        return "Address Block: " + str(self.get_identity_address()) + " (ID) - " + str(self.get_broadcast_address())
    
class Organization:
    def __init__(self, name: str, ip_address_blocks: list[IPAddressBlock] = None):
        self.name: str = name
        self.ip_address_blocks: list[IPAddressBlock] = list(ip_address_blocks) if ip_address_blocks is not None else []
    
    def total_usable_ip_addresses(self):
        return sum([block.get_num_usable_addresses() for block in self.ip_address_blocks])
    
    def __repr__(self):
        return self.name + ": \n" + "\n".join([str(ip_address_block) for ip_address_block in self.ip_address_blocks])
    
class Database:
    def __init__(self):
        self.organizations = []
        