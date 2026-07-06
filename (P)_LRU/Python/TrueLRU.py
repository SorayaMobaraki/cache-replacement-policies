from functools import reduce



class TrueLRU:

    def __init__(self, n_ways, state):
        self.n_ways = n_ways
        self.nBits = (n_ways * (n_ways - 1)) // 2
        self.state_reg = state

    #---------------------------------------------------------------------------------
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
            moreRecentVec.append(state_bin[lsb:lsb + bits_needed].ljust(self.n_ways, '0'))  # left-justify with zeros
            lsb += bits_needed
        
        return moreRecentVec

    #---------------------------------------------------------------------------------
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
            
        
        print(f" state: {state} ")
        # # print(f" final_state_str: {int(result)} ")
        # print(f" moreRecentVec: {moreRecentVec} ")
        # print(f" nextState: {nextState} ")

        
        return result

    

    #---------------------------------------------------------------------------------
    def access(self, touch_way):
        self.state_reg = self.get_next_state(self.state_reg, touch_way)


    #---------------------------------------------------------------------------------
    def access_multiple(self, touch_ways):
        valid_touch_ways = [way for way in touch_ways if way["valid"]]
        if valid_touch_ways:
            self.state_reg = self.get_next_state(self.state_reg, valid_touch_ways[0]["value"])


    #---------------------------------------------------------------------------------
    def get_replace_way(self, state):
        moreRecentVec = self.extractMRUVec(state)
        mruWayDec = []
        for i in range(self.n_ways):
            upperMoreRecent = True if i == self.n_ways - 1 else int(moreRecentVec[i], 2) >> (i + 1) == (1 << (self.n_ways - i - 1)) - 1
            lowerMoreRecent = all((int(e, 2) & (1 << i)) == 0 for e in moreRecentVec)
            mruWayDec.append(upperMoreRecent and lowerMoreRecent)
        # print(f" mruWayDec={mruWayDec}")
        return mruWayDec.index(True)



    #---------------------------------------------------------------------------------
    def way(self):
        return self.get_replace_way(self.state_reg)


    #---------------------------------------------------------------------------------
    def miss(self):
        self.access(self.way())


    #---------------------------------------------------------------------------------
    def hit(self):
        pass
    

    #---------------------------------------------------------------------------------
    def replace(self):
        return self.way()
    



#=======================================================================================
#
#=======================================================================================
class TrueLRU_Printed(TrueLRU):
    def miss(self):
        replaced_way = self.way()
       
        super().miss()
        print(f"Replaced Way: {replaced_way}, Current state_reg: {self.state_reg}")





#=======================================================================================
#
#=======================================================================================
n_way = 4
state = 45
lru_printed = TrueLRU_Printed(n_way, state)

# output = []
# for _ in range(n_way):
#     lru_printed.miss()
#     output.append((lru_printed.way(), lru_printed.state_reg))

# print(f"output is {output}")
# lru_printed.access(7) 
# lru_printed.access(6) 
# lru_printed.access(5)
# lru_printed.access(4)
# lru_printed.access(3)
# lru_printed.access(2)  
# lru_printed.access(1) 
# lru_printed.access(0) 
# lru_printed.access(7) 
# lru_printed.access(6) 
# lru_printed.access(5)
# lru_printed.access(4)
# lru_printed.access(3)
# lru_printed.access(2)  
# lru_printed.access(1) 
# lru_printed.access(0) 

lru_printed.miss()
lru_printed.miss()
lru_printed.miss()
lru_printed.miss()
lru_printed.miss()
lru_printed.miss()
lru_printed.miss()
lru_printed.miss()
lru_printed.miss()
lru_printed.miss()


# lru_printed = TrueLRU_Printed(4)
# lru_printed.miss()
# lru_printed.miss()
# lru_printed.miss()
# lru_printed.miss()
# lru_printed.miss()
# lru_printed.miss()
# lru_printed.miss()
# lru_printed.miss()


#=======================================================================================
#
#=======================================================================================
