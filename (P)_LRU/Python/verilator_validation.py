import re
import pandas as pd
from collections import OrderedDict
from TrueLRU import TrueLRU
from PLRU import PLRUCache


#=======================================================================================
# Extract Address & Hit and Victim Way
#=======================================================================================         
                                 
# Open the Verilator output file and read its content
with open("loop-ROI.txt", "r") as f:
    lines = f.readlines()
with open("python_output.txt", "w") as file:
    pass
with open("Verilator_output.txt", "w") as file:
    pass


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
            #     file.write(str(input_addresses[key]) + '\n')ِ
            
        
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


with open("Verilator_output.txt", "w") as f:      # Write the input addresses and their tags and set the number. Also, the initial LRU state of each set number
    for mapping in sequential_mapping:
        f.write(mapping + "\n")
with open("addresses.txt", "w") as f:
    for address in address_only_list:
        f.write(address + "\n")

 
 
 




#=======================================================================================
# MEMORY
#=======================================================================================                             
class Memory:
    def __init__(self, policy="TrueLRU"):
        self.total_size = 512 * 1024  # 512 kBytes
        self.block_size = 64  # Bytes
        self.set_number = 1024
        self.ways = 8  # Set associative

        self.victim_hit_file = open("Verilator_output.txt", "r")
        
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
        
        # Initialize PLRUCache for each set
        self.lru = {}
        for i in range(self.set_number):
            if policy == "TrueLRU":
                self.lru[i] = TrueLRU(self.ways, 0)
            elif policy == "PLRU":
                self.lru[i] = PLRUCache(self.ways)
                self.lru[i]._assign_indices(self.lru[i].root, [0])
            else:
                raise ValueError(f"Unsupported policy: {policy}")

            
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

        # Check for hit
        hit_keys = [key for key in current_set.keys() if key[0] == details['tag']]
        if hit_keys:
            # there should only be one hit, we take the first key
            hit_key = hit_keys[0]
            _, way = hit_key
            self.lru[details['set']].access(way)
            
            
            #===============================================
            # Write the HitWay of the Python in the File
            #===============================================
            
            for d in hitway_data:
                if (d['Address'] == address and d['Set'] == details['set']):
                    with open("python_output.txt", 'a') as f:  # Open in append mode
                        f.write(f"{address} -> HitWay: {way}, Set: {details['set']}, Tag: {d['Tag']}\n")
                    break  # exit the loop once we've found a match
                    
            

            return "Hit", way, ""

        # check for miss
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
            self.lru[details['set']].access(replace_way)
            
            #===============================================
            # Write the VictimWay of the Python in the File
            #===============================================
           
            for data in victimway_data:
                if (data['Address'] == address) and (data['Set'] == details['set']): 
                    with open("python_output.txt", 'a') as fi:  # Open in append mode
                        fi.write(f"{address} -> VictimWayL2: {replace_way}, Set: {details['set']}, Tag: {data['Tag']}\n")
                    break 
               
                
            # print(f"Miss occurred for address {address}. Set: {details['set']}, VictimWayL2: {replace_way}, LRU state: {lru_state}")     #to print when victim happen
            return "Miss", replace_way, eviction_status
            
            
    
            
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


#=======================================================================================
#
# COMPARISON OF VERILATOR AND PYTHON OUTPUT
#
#=======================================================================================

def parse_line(line):
    parts = line.split(' -> ')
    address = parts[0]
    details = parts[1].split(', ')
    type_part = details[0].split(': ')
    way_type = type_part[0]
    way_number = int(type_part[1])
    set_value = int(details[1].split(': ')[1])
    tag = int(details[2].split(': ')[1])
    lru_state = None
    if len(details) > 3:
        lru_state = int(details[3].split(': ')[1])

    return address, way_type, way_number, set_value, tag, lru_state


data1 = []
with open('python_output.txt', 'r') as file:
    for line in file:
        data1.append(parse_line(line.strip()))

df_python = pd.DataFrame(data1, columns=['Address', 'Type', 'TypeNumber', 'Set', 'Tag', 'LRUstate'])
df_python = df_python.drop('LRUstate', axis=1)

pd.set_option('display.max_rows', None)
print("Python Output:")
print(df_python)
print("-"*50)

data2 = []
with open('Verilator_output.txt', 'r') as file:
    for line in file:
        data2.append(parse_line(line.strip()))

df_verilator = pd.DataFrame(data2, columns=['Address', 'Type', 'TypeNumber', 'Set', 'Tag', 'LRUstate'])
df_verilator = df_verilator.drop('LRUstate', axis=1)
print("Verilator Output:")
print(df_verilator)

print("*"*50)
if df_python.equals(df_verilator):
    print("Python and verilator outputs are equal")
else:
    print("Python and verilator outputs are Not equal")
    
differences = df_python.compare(df_verilator)
# print("Differences:" ,differences)

