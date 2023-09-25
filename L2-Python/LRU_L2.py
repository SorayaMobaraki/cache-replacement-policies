import re

from collections import OrderedDict


# def extract_addresses():
#     # Regular expressions to match the patterns "SourceA:address:" and "L1D -> L2: ReleaseData: addr ="
#     sourceA_pattern = re.compile(r"SourceA:address:(0x[0-9a-fA-F]+)")
#     releaseData_pattern = re.compile(r"L1D -> L2: ReleaseData: addr = (0x[0-9a-fA-F]+)")

#     # Open the input file for reading and the output file for writing
#     with open("loop-ROI.txt", 'r') as infile, open("addresses.txt", 'w') as outfile:
#         last_address = None  # Store the last seen address for "L1D -> L2: ReleaseData: addr ="
#         for line in infile:
#             # Check for SourceA pattern
#             sourceA_match = sourceA_pattern.search(line)
#             if sourceA_match:
#                 outfile.write(sourceA_match.group(1) + '\n')
            
#             # Check for ReleaseData pattern
#             releaseData_match = releaseData_pattern.search(line)
#             if releaseData_match:
#                 current_address = releaseData_match.group(1)
#                 if current_address != last_address:  # Check if the current address is different from the last seen address
#                     outfile.write(current_address + '\n')
#                 last_address = current_address


#=======================================================================================
# Extract Address& Hit and Victim Way
#=======================================================================================         
                
                
acquire_pattern = re.compile(r"L1D -> L2: Acquire: addr = (0x[0-9a-fA-F]+)")
releaseData_pattern = re.compile(r"L1D -> L2: ReleaseData: addr = (0x[0-9a-fA-F]+)")
hitway_pattern = re.compile(r'HitWay:\s*(\d+)')
victimwayl2_pattern = re.compile(r'VictimWayL2:\s*(\d+)')
set_pattern = re.compile(r'set:\s*(\d+)')

def extract_addresses_and_hitways(input_file="loop-ROI.txt", patterns_to_extract=["acquire", "release", "hitway", "victimwayl2"], 
                                  address_output="addresses.txt", paired_output="address_with_hitway.txt"):
    
    with open(input_file, 'r') as infile, \
         open(address_output, 'w') as outfile1, \
         open(paired_output, 'w') as outfile2:

        address_queue = []
        last_address = None

        for line in infile:
            # Check for Acquire pattern
            if "acquire" in patterns_to_extract:
                acquire_match = acquire_pattern.search(line)
                if acquire_match:
                    address_queue.append(acquire_match.group(1))
                    outfile1.write(acquire_match.group(1) + '\n')

            # Check for ReleaseData pattern
            if "release" in patterns_to_extract:
                releaseData_match = releaseData_pattern.search(line)
                if releaseData_match:
                    current_address = releaseData_match.group(1)
                    if current_address != last_address:  # Only consider the address if it's different from the last one
                        address_queue.append(current_address)
                        outfile1.write(current_address + '\n')
                    last_address = current_address

            # Check for HitWay and set patterns
            if "hitway" in patterns_to_extract:
                hitway_match = hitway_pattern.search(line)
                set_match = set_pattern.search(line)
                if hitway_match and set_match and address_queue:
                    hitway = hitway_match.group(1)
                    set_number = set_match.group(1)
                    outfile2.write(f"{address_queue.pop(0)} -> HitWay: {hitway}, Set: {set_number}\n")

            # Check for VictimWayL2 and set patterns
            if "victimwayl2" in patterns_to_extract:
                victimwayl2_match = victimwayl2_pattern.search(line)
                set_match = set_pattern.search(line)
                if victimwayl2_match and set_match and address_queue:
                    victimwayl2 = victimwayl2_match.group(1)
                    set_number = set_match.group(1)
                    outfile2.write(f"{address_queue.pop(0)} -> VictimWayL2: {victimwayl2}, Set: {set_number}\n")




 
#=======================================================================================

extract_addresses_and_hitways()

 
#=======================================================================================

#Find the address and set of each victimwayl2 that has been extracted
address_to_victimwayl2 = {}

with open("address_with_hitway.txt", "r") as file:
    for line in file:
        if "VictimWayL2" in line:
            address, way_info = line.strip().split(" -> ")
            victimwayl2_value = int(way_info.split(": ")[1].split(",")[0])
            set_value = int(way_info.split("Set: ")[1])
            address_to_victimwayl2[address] = (victimwayl2_value, set_value)




address_to_hitway = {}
#Find the address of each HitWay that has been extracted
with open("address_with_hitway.txt", "r") as file:
    for line in file:
        if "HitWay" in line:
            address, way_info = line.strip().split(" -> ")
            hitway = int(way_info.split(": ")[1].split(",")[0])
            set_value = int(way_info.split("Set: ")[1])
            address_to_hitway[address] = hitway

 
 
#=======================================================================================
# MEMORY
#=======================================================================================                             
class Memory:
    def __init__(self):
        # Given specifications
        self.total_size = 512 * 1024  # 512 kBytes
        self.block_size = 64  # Bytes
        self.set_number = 1024
        self.ways = 8  # Set associative
        
        
        self.victim_hit_file = open("address_with_hitway.txt", "r")
        
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
        
        # Initialize TrueLRU for each set
        self.lru = {}
        for i in range(self.set_number):
            self.lru[i] = TrueLRU(self.ways, 0)  # Starting with state 0 for simplicity
    
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
        
        lru_state = self.lru[details['set']].state_reg

        # Check for hit
        hit_keys = [key for key in current_set.keys() if key[0] == details['tag']]
        if hit_keys:
            # there should only be one hit, we take the first key
            hit_key = hit_keys[0]
            _, way = hit_key
            self.lru[details['set']].hit(way)
            # print(f"Hit occurred for address {address}. Set: {details['set']}, Hitway: {way}, LRU state: {lru_state}")
            if address in address_to_hitway:
                expected_hit_way = address_to_hitway[address]
                if expected_hit_way == way:
                    print(f"Address: {address}, Set: {details['set']}, Verilator HitWay: {expected_hit_way}, Python Hitway: {way} -> Equal")
                else:
                    print(f"Address: {address}, Set: {details['set']}, Verilator HitWay: {expected_hit_way}, Python Hitway: {way} -> Not Equal")
            
            return "Hit", way, ""
        else:
            # On a miss, get the LRU way to replace
            replace_way = self.lru[details['set']].way()
            if replace_way in [key[1] for key in current_set.keys()]:
                # If the replace way is already in the set, evict it
                evicted_key = [key for key in current_set.keys() if key[1] == replace_way][0]
                current_set.pop(evicted_key)
                eviction_status = "eviction"
            else:
                eviction_status = ""
            
            # Update cache with new block
            current_set[(details['tag'], replace_way)] = details['tag']
            self.lru[details['set']].miss()  # Inform LRU of a miss
            
            # line = self.victim_hit_file.readline()
            # if "VictimWayL2" in line:
            #     victim_way = int(line.split("VictimWayL2:")[-1].strip())
                
            #     # Compare replace_way with victim_way
            #     if replace_way == victim_way:
            #         print(f"Address: {address}, Set: {details['set']}. Python Replace way ({replace_way}) matches with extracted VictimWayL2 in Verilator ({victim_way}).")
            #     else:
            #         print(f"Address: {address}, Set: {details['set']}. Python Replace way ({replace_way}) does not match with extracted VictimWayL2 in Verilator ({victim_way}).")
            
        
            # print(f"Miss occurred for address {address}. Set: {details['set']}, Replacing way: {replace_way}, LRU state: {lru_state}")
            
            # if address in address_to_victimwayl2:
            #     expected_victim_way = address_to_victimwayl2[address][0]
            #     if expected_victim_way == replace_way:
            #         print(f"Address: {address}, Set: {details['set']}, Verilator VictimWayL2: {expected_victim_way}, Python replace_way: {replace_way} -> Equal")
            #     else:
            #         print(f"Address: {address}, Set: {details['set']}, Verilator VictimWayL2: {expected_victim_way}, Python replace_way: {replace_way} -> Not Equal")
                    
                
            # # print(f"Miss occurred for address {address}. Set: {details['set']}, VictimWayL2: {replace_way}")
            return "Miss", replace_way, eviction_status
            



def extract_HitOrMiss(filename="loop-ROI.txt"):
    with open(filename, 'r') as f:
        content = f.read()

        victimwayl2_match = re.search(r'VictimWayL2:\s*(\d+)', content)
        hitway_match = re.search(r'HitWay:\s*(\d+)', content)

        victimwayl2_value = int(victimwayl2_match.group(1)) if victimwayl2_match else None
        hitway_value = int(hitway_match.group(1)) if hitway_match else None

        return victimwayl2_value, hitway_value


#=======================================================================================
#
#=======================================================================================
class TrueLRU:

    def __init__(self, n_ways, state):
        self.n_ways = n_ways
        self.nBits = (n_ways * (n_ways - 1)) // 2
        self.state_reg = state

    def UIntToOH(self, value, width):
        return [1 if i == value else 0 for i in range(width)]
    #---------------------------------------------------------------------------------
    
    def OHToUInt(self, oh_list):
        for i, bit in enumerate(oh_list):
            if bit:
                return i
        return 0
    #---------------------------------------------------------------------------------

    
    def extractMRUVec(self, state):
        state_bin = bin(state)[2:].zfill(self.nBits)  
        moreRecentVec = []
        lsb = 0
        for i in range(self.n_ways - 1):
            bits_needed = self.n_ways - i - 1
            moreRecentVec.append(state_bin[lsb:lsb + bits_needed].ljust(self.n_ways, '0'))
            lsb += bits_needed
        return moreRecentVec
    
#=======================================================================================
#
#=======================================================================================

    def get_next_state(self, state: int, touch_way: int):
        moreRecentVec = self.extractMRUVec(state)
        wayDec = 1 << touch_way
        nextState = []
        for i in range(self.n_ways - 1):
            if i == touch_way:
                nextState.append(0)
            else:
                nextState.append(int(moreRecentVec[i], 2) | wayDec)
        result = nextState[0] >> 1
        for i in range(1, self.n_ways - 1):
            result = (result << (self.n_ways - i - 1)) | (nextState[i] >> (i + 1))
        # print(f" state: {state} ")
        return result

    def access(self, touch_way):
        self.state_reg = self.get_next_state(self.state_reg, touch_way)

    def access_multiple(self, touch_ways):
        valid_touch_ways = [way for way in touch_ways if way["valid"]]
        if valid_touch_ways:
            self.state_reg = self.get_next_state(self.state_reg, valid_touch_ways[0]["value"])
            
#=======================================================================================
#
#=======================================================================================
    def get_replace_way(self, state):
        moreRecentVec = self.extractMRUVec(state)
        mruWayDec = []
        for i in range(self.n_ways):
            upperMoreRecent = True if i == self.n_ways - 1 else int(moreRecentVec[i], 2) >> (i + 1) == (1 << (self.n_ways - i - 1)) - 1
            lowerMoreRecent = all((int(e, 2) & (1 << i)) == 0 for e in moreRecentVec)
            mruWayDec.append(upperMoreRecent and lowerMoreRecent)
        return mruWayDec.index(True)
    
#=======================================================================================
#
#=======================================================================================

    def way(self):
        return self.get_replace_way(self.state_reg)

    def miss(self):
        self.access(self.way())

    def hit(self, hit_way):
        self.state_reg = self.get_next_state(self.state_reg, hit_way)


    def replace(self):
        return self.way()

            



memory = Memory()


print(f"Number of blocks: {memory.blocks}")

# Reading addresses from the file
with open("addresses.txt", "r") as file:
    addresses = [line.strip() for line in file]

for address in addresses:
    hit_or_miss, way, eviction_occurred = memory.access(address)

    result = memory.extract(address)
    eviction_message = "         VictimWayL2" if eviction_occurred == "eviction" else ""
    
    # print(f"Address: {address}, Set: {result['set']}, {hit_or_miss}, Way: {way}{eviction_message}")




