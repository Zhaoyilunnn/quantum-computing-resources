import sys
import numpy as np
from quafu import QuantumCircuit, Task, User, simulate

# user = User()
##user.save_apitoken("4DEH53vA_IxMSg_fyZ3grsJ4ew7Jn-itMS6bcPlJ7E9.Qf0UzM1QDNwgjNxojIwhXZiwSO2ITM6ICZpJye.9JiN1IzUIJiOicGbhJCLiQ1VKJiOiAXe0Jye")
# user.save_apitoken("4039_bwgVySvM-QmTJzvRwpx3HH_dEA6Y012on_pSAp.QfyITM2YDO1gjNxojIwhXZiwSO2ITM6ICZpJye.9JiN1IzUIJiOicGbhJCLiQ1VKJiOiAXe0Jye")

GROUP_NAME = "zhaoyilun"

if __name__ == "__main__":
    measure_only = 0
    if len(sys.argv) == 2:
        measure_only = int(sys.argv[1])

    q = QuantumCircuit(2)
    if not measure_only:
        q.h(0)
        q.cnot(0, 1)

    measures = [0, 1]
    cbits = [0, 1]
    q.measure(measures, cbits=cbits)
    # q.unitary(np.array([[0, 1],[1, 0]]), [0])
    q.draw_circuit()
    res = simulate(q)
    res.plot_probabilities()

    # task = Task()
    # info = task.get_backend_info()
    # task.config(backend="ScQ-P136", shots=2000, compile=True)
    # task.load_account()


    # res = task.send(q, wait=False, name="zhaoyilun-test", group=GROUP_NAME)
    # group_res = task.retrieve_group(GROUP_NAME)
    # print(group_res)
    # res = task.send(q, wait=True)
    # print(res)
