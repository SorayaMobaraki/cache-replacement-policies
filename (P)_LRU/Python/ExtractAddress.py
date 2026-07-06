import re

# Regular expressions to match the patterns "SourceA:address:" and "L1D -> L2: ReleaseData: addr ="
sourceA_pattern = re.compile(r"SourceA:address:(0x[0-9a-fA-F]+)")
releaseData_pattern = re.compile(r"L1D -> L2: ReleaseData: addr = (0x[0-9a-fA-F]+)")

# Open the input file for reading and the output file for writing
with open("loop-ROI.txt", 'r') as infile, open("addresses.txt", 'w') as outfile:
    last_address = None  # Store the last seen address for "L1D -> L2: ReleaseData: addr ="
    for line in infile:
        # Check for SourceA pattern
        sourceA_match = sourceA_pattern.search(line)
        if sourceA_match:
            outfile.write(sourceA_match.group(1) + '\n')
        
        # Check for ReleaseData pattern
        releaseData_match = releaseData_pattern.search(line)
        if releaseData_match:
            current_address = releaseData_match.group(1)
            if current_address != last_address:  # Check if the current address is different from the last seen address
                outfile.write(current_address + '\n')
            last_address = current_address  # Update the last seen address
