# Phython_code_to_compare_Verilator_Output
In this repository You can find the Python codes for [L2cache](https://gite.lirmm.fr/smobaraki/phython_code_to_compare_verilator_output/-/blob/main/L2-Python/L2cache.py?ref_type=heads), [Extract addresses](https://gite.lirmm.fr/smobaraki/phython_code_to_compare_verilator_output/-/blob/main/L2-Python/ExtractAddress.py?ref_type=heads) from the Output, [LRU code that transfered from Chisel](https://gite.lirmm.fr/smobaraki/phython_code_to_compare_verilator_output/-/blob/main/L2-Python/TrueLRU.py?ref_type=heads), L2cahe with [LRU in OrderDict with L2 cache](https://gite.lirmm.fr/smobaraki/phython_code_to_compare_verilator_output/-/blob/main/L2-Python/LRU-OrderedDict.py?ref_type=heads), and also [transfered_LRU of the Chisel with Extract address and Cache inside](https://gite.lirmm.fr/smobaraki/phython_code_to_compare_verilator_output/-/blob/main/L2-Python/LRU_L2.py?ref_type=heads).


From the ablove codes you just need the [LRU_L2](https://gite.lirmm.fr/smobaraki/phython_code_to_compare_verilator_output/-/blob/main/L2-Python/LRU_L2.py?ref_type=heads).



## Change the Chisel code 
We need to change the Chisel code in the verilator to Extract and compare the Python and Verilator results Automatically.



### In the Rocket/Dcache.scala

You need to put these lines in the Dcache because they are necessary to compare the addresses and the set number of the instructions sent from L1 to L2 with the Set numbers that will have hit or miss.

    when((tl_out.a.bits.opcode === UInt(6)) && tl_out.a.valid && tl_out.a.ready) {
      printf(" L1D -> L2: Acquire: addr = 0x%x, set:%d\n", tl_out.a.bits.address, (tl_out.a.bits.address >> 6) & "b00001111111111".U)
    }
    when(dataArb.io.out.ready && dataArb.io.out.valid) {
      when(dataArb.io.out.bits.write) {
        printf("VictimWayL1: %b, Refilling set: %d, L1_dirty:%d\n", dataArb.io.out.bits.way_en, dataArb.io.out.bits.addr >> 6, s2_victim_dirty)
      }
    }

    when((tl_out.c.bits.opcode === UInt(7)) && tl_out.c.valid && tl_out.c.ready) {
      printf("    L1D -> L2: ReleaseData: addr = 0x%x, set:%d, data = 0x%x\n", tl_out.c.bits.address, (tl_out.a.bits.address >> 6) & "b00001111111111".U, tl_out.c.bits.data)
    }



### In the Inclusivecache/Directory

In the Directory you need to print this lines, becuse for our extraction and then comparation wee need them. You can also find the final Directory code [here](https://gite.lirmm.fr/smobaraki/l2cache/-/blob/master/Directory.scala?ref_type=heads).


    when(io.result.valid) {
        when (missCond) {
        printf("VictimWayL2:%d, wayMatch: %d, io.result.bits.hit: %d, io.result.bits.way:%d, set:%d, array_rep:%d\n", victimWay, wayMatch, io.result.bits.hit, io.result.bits.way, readSetReg, array_rep)
        }.otherwise{
        printf("HitWay:%d, wayMatch: %d, io.result.bits.hit:%d, io.result.bits.way:%d, set:%d, array_rep:%d\n", OHToUInt(hits), wayMatch, io.result.bits.hit, io.result.bits.way, readSetReg, array_rep)
        }
    }

