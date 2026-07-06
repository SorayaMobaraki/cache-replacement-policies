class Memory:
    def __init__(self):
        # Given specifications
        self.total_size = 512 * 1024  # 512 kBytes
        self.block_size = 64  # Bytes
        self.set_number = 1024
        self.ways = 8  # Set associative

        # Calculate number of blocks
        self.blocks = self.total_size / self.block_size
        
    
        
        # Calculate bits needed for offset, set, and tag
        self.offset_bits = int(self.log2(self.block_size))
        self.set_bits = int(self.log2(self.set_number))
        self.tag_bits = 32 - self.offset_bits - self.set_bits  # Assuming 32-bit addresses

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


memory = Memory()

print(f"Number of blocks: {memory.blocks}")

# Reading addresses from the file
with open("addresses.txt", "r") as file:
    addresses = [line.strip() for line in file]

for address in addresses:
    result = memory.extract(address)
    print(f"For address: {address}, Tag: {result['tag']}, Set: {result['set']}, Offset: {result['offset']}\n")
