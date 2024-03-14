from myhdl import block, always_comb, Signal, instance, intbv

@block
def instruction_router(instruction, output_signals):
    """
    A simple instruction router.
    - instruction: Input signal representing instruction sequences.
    - output_signals: A list of output signals for different FPGAs.
    """
    # Assuming each instruction is 3 bits and maps directly to an FPGA
    NUM_FPGAS = len(output_signals)

    @always_comb
    def router_logic():
        # Initialize all outputs to zero
        for sig in output_signals:
            sig.next = 0

        # Based on the instruction, activate the corresponding FPGA signal
        if instruction < NUM_FPGAS:
            output_signals[instruction].next = 1

    return router_logic

# Example usage
from myhdl import Simulation, delay

def test():
    instruction = Signal(intbv(0)[3:])  # 3-bit instruction
    outputs = [Signal(intbv(0)[1:]) for _ in range(4)]  # 4 FPGAs

    inst_router = instruction_router(instruction, outputs)

    @block
    def testbench():
        @instance
        def stimulus():
            for i in range(8):
                instruction.next = i
                yield delay(10)
                print(f'Instruction: {instruction}, Outputs: {[o.val for o in outputs]}')

        return stimulus

    sim = Simulation(inst_router, testbench())
    sim.run()

# Running the test
if __name__ == '__main__':
    test()
