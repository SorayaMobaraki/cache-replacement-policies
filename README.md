# Phython_code_to_compare_Verilator_Output
In this repository, You can find the Python codes for [L2cache](https://gite.lirmm.fr/smobaraki/phython_code_to_compare_verilator_output/-/blob/main/L2-Python/L2cache.py?ref_type=heads), [Extract addresses](https://gite.lirmm.fr/smobaraki/phython_code_to_compare_verilator_output/-/blob/main/L2-Python/ExtractAddress.py?ref_type=heads) from the Output, [LRU code that transferred from Chisel](https://gite.lirmm.fr/smobaraki/phython_code_to_compare_verilator_output/-/blob/main/L2-Python/TrueLRU.py?ref_type=heads), L2cahe with [LRU in OrderDict with L2 cache](https://gite.lirmm.fr/smobaraki/phython_code_to_compare_verilator_output/-/blob/main/L2-Python/LRU-OrderedDict.py?ref_type=heads), and also LRU_L2 [the transfered_LRU of the Chisel with Extract address and Cache inside](https://gite.lirmm.fr/smobaraki/phython_code_to_compare_verilator_output/-/blob/main/L2-Python/LRU_L2.py?ref_type=heads).


From the above codes, you need the [LRU_L2](https://gite.lirmm.fr/smobaraki/phython_code_to_compare_verilator_output/-/blob/main/L2-Python/LRU_L2.py?ref_type=heads) to extract and compare. In this Python code, you can see the ways that have miss or hit, and you also can compare the LRU output in Verilator with the LRU output in the Python one.



## Change the Chisel code 
We need to change the Chisel code in the verilator to Extract and compare the Python and Verilator results Automatically.



### In the Rocket/Dcache.scala

You need to put these lines in the Dcache because you can see the addresses and the set number of the instructions sent from L1D to L2 with the Set numbers that will have hit or miss.

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

### In the SinkA.scala and SinkC.scala

You need to put these lines to print in these two files.

SinkA:

  
    //Sm*********************
    val (tag_io, set_io, offset_io) = params.parseAddress(io.a.bits.address)
    printf("SinkA:address:0x%x, set:%d, tag:%d\n", io.a.bits.address, set_io, tag_io)
    //



SinkC:

    //Sm*********************
    val (tag_io, set_io, offset_io) = params.parseAddress(io.c.bits.address)

    printf("SinkC:address:0x%x, set:%d, tag:%d\n", io.c.bits.address, set_io, tag_io)
    //




### In the Inclusivecache/Directory

In the Directory you need to print these lines, because for our extraction and then comparison we need them. You can also find the final Directory code [here](https://gite.lirmm.fr/smobaraki/l2cache/-/blob/master/Directory.scala?ref_type=heads).


  //Sm

  when(io.result.valid) {
    when (missCond) {
      printf("VictimWayL2:%d, wayMatch: %d, io.result.bits.hit: %d, io.result.bits.way:%d, set:%d, tag:%d, lrustate:%d\n", victimWay, wayMatch, io.result.bits.hit, io.result.bits.way, readSetReg, readTagReg , array_rep)
    }.otherwise{
      printf("HitWay:%d, wayMatch: %d, io.result.bits.hit:%d, io.result.bits.way:%d, set:%d, tag:%d, lrustate:%d\n", OHToUInt(hits), wayMatch, io.result.bits.hit, io.result.bits.way, readSetReg, readTagReg , array_rep)
    }
  }
  ///

