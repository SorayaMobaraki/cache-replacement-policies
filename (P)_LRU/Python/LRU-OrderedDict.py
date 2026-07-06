from collections import OrderedDict

class Memory:
    def __init__(self):
        # Given specifications
        self.total_size = 512 * 1024  # 512 kBytes
        self.block_size = 64  # Bytes
        self.set_number = 1024
        self.ways = 8  # Set associative
        
        self.last_way_used = {}  # This will track the last way 
        
        # Calculate number of blocks
        self.blocks = self.total_size / self.block_size
        
        # Calculate bits needed for offset, set, and tag
        self.offset_bits = int(self.log2(self.block_size))
        self.set_bits = int(self.log2(self.set_number))
        self.tag_bits = 32 - self.offset_bits - self.set_bits  # Assuming 32-bit addresses

        # Cache implementation using OrderedDict
        # Each key in the OrderedDict will be a tuple (tag, way)
        self.cache = {}
        for i in range(self.set_number):
            
            self.cache[i] = OrderedDict()
    
    @staticmethod
    def log2(x):
        return x.bit_length() - 1

    def extract(self, address):
        address_bin = bin(int(address, 16))[2:].zfill(32)
        
        tag = address_bin[:self.tag_bits]
        set_ = address_bin[self.tag_bits:self.tag_bits + self.set_bits]
        offset = address_bin[self.tag_bits + self.set_bits:]
        
        return {
            'tag': int(tag, 2),
            'set': int(set_, 2),
            'offset': int(offset, 2)
        }

    def access(self, address):
        details = self.extract(address)
        current_set = self.cache[details['set']]

        # Check for hit
        hit_keys = [key for key in current_set.keys() if key[0] == details['tag']]
        if hit_keys:
            # Since there should only be one hit, we take the first key
            hit_key = hit_keys[0]
            current_set.move_to_end(hit_key)
            _, way = hit_key
            return "Hit", way, ""
        else:
            # Check for miss and possible eviction
            if len(current_set) == self.ways:
                # Cache is full, need to evict
                evicted_key = next(iter(current_set.keys()))  # get the first (least recently used) key
                _, evicted_way = evicted_key
                current_set.pop(evicted_key)  # remove this least recently used block
                current_set[(details['tag'], evicted_way)] = details['tag']  # Insert the new block in the evicted way
                return "Miss", evicted_way, "eviction"
            else:
                # Cache has space, find the next available way
                available_way = len(current_set)
                current_set[(details['tag'], available_way)] = details['tag']
                return "Miss", available_way, ""






memory = Memory()

print(f"Number of blocks: {memory.blocks}")

# Reading addresses from the file
with open("addresses.txt", "r") as file:
    addresses = [line.strip() for line in file]

for address in addresses:
    hit_or_miss, way, eviction_occurred = memory.access(address)

    result = memory.extract(address)
    eviction_message = "         VictimWayL2" if eviction_occurred == "eviction" else ""
    
    print(f"Address: {address}, Set: {result['set']}, {hit_or_miss}, Way: {way}{eviction_message}")




