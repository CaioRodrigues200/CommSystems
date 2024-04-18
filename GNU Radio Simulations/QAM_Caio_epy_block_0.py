"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, M=4, Ep=1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='QAM_Modulator_Caio',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.M = M
        self.Ep = Ep

    def work(self, input_items, output_items):
        N = int(np.sqrt(self.M)/2)
        BNum = int(np.log2(self.M))
        oneDim = np.arange(-1 - 2*(N-1) , 1 + 2*(N-1) + 2, 2)

        ConstPts = np.zeros((self.M),dtype=np.complex64)
        bitArray = np.zeros((self.M*2*N))
        OutArray = np.zeros((int(len(input_items[0]))),dtype=np.complex64)
        SEnergy = 0

        for i in range(2*N):
            for j in range(2*N):
                ConstPts[int(j+i*(2*N))] = oneDim[i]+1j*oneDim[j]
                SEnergy = SEnergy + oneDim[i]**2+oneDim[j]**2
        SEnergy = SEnergy/self.M
        ConstPts = self.Ep*ConstPts/SEnergy

        seq = np.arange(self.M)
        bitArray = [np.binary_repr(x,BNum) for x in seq]

        output_items[0][:] = np.array(list(map(int,input_items[0])))

        for i in range(int(len(input_items[0])/BNum)):
            for j in range(self.M):
                if(''.join(list(map(str,(np.array(list(map(int,input_items[0][i*BNum : (i+1)*BNum]))))))) == bitArray[j]):
                    OutArray[i*BNum : (i+1)*BNum] = np.pad(ConstPts[j],(0,BNum-1))
                    break
        
        output_items[0][:] = OutArray
        return len(output_items[0])
    

    # def work(self, input_items, output_items):
    #     """example: multiply with constant"""
    #     output_items[0][:] = input_items[0] * self.M
    #     return len(output_items[0])
