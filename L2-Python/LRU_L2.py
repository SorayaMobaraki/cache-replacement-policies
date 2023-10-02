import re

from collections import OrderedDict


#=======================================================================================
# Extract Address & Hit and Victim Way
#=======================================================================================         
                
                
# Open the Verilator output file and read its content
with open("Loop-ROI.txt", "r") as f:
    lines = f.readlines()


# Regular expression patterns
sink_a_pattern = re.compile(r"SinkA:address:(0x[0-9a-fA-F]+).*set:\s+(\d+).*tag:(\d+)")
sink_c_pattern = re.compile(r"SinkC:address:(0x[0-9a-fA-F]+).*set:\s+(\d+).*tag:(\d+)")
victim_pattern = re.compile(r"VictimWayL2:(\d+).*set:\s+(\d+).*tag:(\d+),\s*lrustate:\s*(\d+)")
hit_pattern = re.compile(r"HitWay:(\d+).*set:\s+(\d+).*tag:(\d+),\s*lrustate:\s*(\d+)")

input_addresses = {}
# source_c_addresses = {}
victimway_data = []
hitway_data = []

# Extracting SinkA and SinkC addresses (as input addresses) using regex
for line in lines:
    match_a = sink_a_pattern.search(line)
    match_c = sink_c_pattern.search(line)
    if match_a:
        address, set_val, tag_val = match_a.groups()
        input_addresses[(int(set_val), int(tag_val))] = address
    if match_c:
        address, set_val, tag_val = match_c.groups()
        input_addresses[(int(set_val), int(tag_val))] = address

# Re-extracting sequential mapping and addresses using regex
sequential_mapping = []
address_only_list = []
encountered_sets = set()


for line in lines:
    match_victim = victim_pattern.search(line)
    match_hit = hit_pattern.search(line)
    if match_victim:
        way, set_val, tag_val, lrustate = map(int, match_victim.groups())
        key = (set_val, tag_val)
        if key in input_addresses:
            if set_val not in encountered_sets:   #this is to be sure that just the initial lru state write in the file
                encountered_sets.add(set_val)
                newlrustate = lrustate if lrustate is not None else "Unknown"
                mapping_str = f"{input_addresses[key]} -> VictimWayL2: {way}, Set: {set_val}, Tag: {tag_val}, LRUstate: {newlrustate}"
            else: 
                mapping_str = f"{input_addresses[key]} -> VictimWayL2: {way}, Set: {set_val}, Tag: {tag_val}"
            
            # with open('address1.txt', 'a') as file:
            #     file.write(str(input_addresses[key]) + '\n')
            
        
            victimway_data.append({            # a list of dictionary to extract the address, set, tag, and Lru state of the victimway
                'Address': input_addresses[key],
                'VictimWay': way,
                'Set': set_val,
                'Tag': tag_val,
                'LRUstate': newlrustate
            })

            sequential_mapping.append(mapping_str)
            address_only_list.append(input_addresses[key])
    if match_hit:
        way, set_val, tag_val, lrustate = map(int, match_hit.groups())
        key = (set_val, tag_val)
        if key in input_addresses:
            if set_val not in encountered_sets:    #this is to be sure tht just the initial lru state write in the file
                encountered_sets.add(set_val)
                newlrustate = lrustate if lrustate is not None else "Unknown"
                mapping_str = f"{input_addresses[key]} -> HitWay: {way}, Set: {set_val}, Tag: {tag_val}, LRUstate: {newlrustate}"
            else:
                mapping_str = f"{input_addresses[key]} -> HitWay: {way}, Set: {set_val}, Tag: {tag_val}"
            # with open('address1.txt', 'a') as file:
            #     file.write(str(input_addresses[key]) + '\n')
                
            
            hitway_data.append({            # a list of dictionary to extract the address, set, tag, and Lru state of the Hitway
                'Address': input_addresses[key],
                'HitWay': way,
                'Set': set_val,
                'Tag': tag_val,
                'LRUstate': newlrustate
            })

            sequential_mapping.append(mapping_str)
            address_only_list.append(input_addresses[key])


with open("address_with_hitway.txt", "w") as f:      # Write the input addresses and their tags and set the number. Also, the initial LRU state of each set number
    for mapping in sequential_mapping:
        f.write(mapping + "\n")
with open("addresses.txt", "w") as f:
    for address in address_only_list:
        f.write(address + "\n")

 
#=======================================================================================
# MEMORY
#=======================================================================================                             
class Memory:
    def __init__(self):
       
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
            initialized = False  # To track if the LRU for set 'i' has been initialized
            # for m in hitway_data + victimway_data:  # Combine both lists for processing
            #     if m["Set"] == i:
            #         initial_state = m['LRUstate'] if m['LRUstate'] is not None else 0
            #         self.lru[i] = TrueLRU(self.ways, initial_state)
            #         initialized = True
            #         break  # break the inner loop once LRU for set 'i' is initialized
            if not initialized:  # if the LRU for set 'i' was not initialized befor ( in iner loop)
                self.lru[i] = TrueLRU(self.ways, 0)

            
    @staticmethod
    def log2(x):
        return x.bit_length() - 1

    def extract(self, address):       #extract the addres of new instructions
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

        ### Check for hit
        hit_keys = [key for key in current_set.keys() if key[0] == details['tag']]
        if hit_keys:
            # there should only be one hit, we take the first key
            hit_key = hit_keys[0]
            _, way = hit_key
            self.lru[details['set']].hit(way)
            # print(f"Hit occurred for address {address}. Set: {details['set']}, Hitway: {way}, LRU state: {lru_state}")

            #===============================================
            #Check if the Verilator HitWay is equal to Python
            #===============================================
            # for d in hitway_data:
            #     if d['Address'] == address and d['Set'] == details['set']:
            #         if d['HitWay'] == way:
            #             print(f"Address: {address}, Set: {details['set']}, Tag: {details['tag']}, Verilator HitWay: {d['HitWay'] }, Python HitWay: {way} -> Equal")
            #         else:
            #             print(f"Address: {address}, Set: {details['set']}, Tag: {details['tag']}, Verilator HitWay: {d['HitWay'] }, Python HitWay: {way} -> Not Equal")
            #         break  # exit the loop once we've found a match
            
            
           
            # print(f"Hit occurred for address {address}. Set: {details['set']}, HitWay: {way}, LRU state: {lru_state}")      # to print when hit happen   
            return "Hit", way, ""
        
        ### check for miss
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
            
            #===============================================
            #Check if the Verilator VictimWay is equal to Python
            #===============================================
           
            for data in victimway_data:

                if (data['Address'] == address) and (data['Set'] == details['set']): 
                    if (data['VictimWay']  == replace_way):
                        print(f"Address: {address}, Set: {details['set']}, Tag: {details['tag']}, Verilator VictimWayL2: {data['VictimWay'] }, Python replace_way: {replace_way} -> Equal")
                    else:
                        print(f"Address: {address}, Set: {details['set']}, Tag: {details['tag']}, Verilator VictimWayL2: {data['VictimWay'] }, Python replace_way: {replace_way} -> Not Equal")
                    break 
               
                
            # print(f"Miss occurred for address {address}. Set: {details['set']}, VictimWayL2: {replace_way}, LRU state: {lru_state}")     #to print when victim happen
            return "Miss", replace_way, eviction_status
            


#=======================================================================================
#  TrueLRU
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
    # get_next_state
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
    #get_replace_way
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

   
            
#=======================================================================================
#=======================================================================================
#=======================================================================================

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




