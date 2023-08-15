import sys
import numpy as np
from quafu import QuantumCircuit, Task, User

#user = User()
##user.save_apitoken("4DEH53vA_IxMSg_fyZ3grsJ4ew7Jn-itMS6bcPlJ7E9.Qf0UzM1QDNwgjNxojIwhXZiwSO2ITM6ICZpJye.9JiN1IzUIJiOicGbhJCLiQ1VKJiOiAXe0Jye")
#user.save_apitoken("4039_bwgVySvM-QmTJzvRwpx3HH_dEA6Y012on_pSAp.QfyITM2YDO1gjNxojIwhXZiwSO2ITM6ICZpJye.9JiN1IzUIJiOicGbhJCLiQ1VKJiOiAXe0Jye")

GROUP_NAME = "zhaoyilun"

if __name__ == '__main__':

    run = 1
    if len(sys.argv) == 2:
        run = int(sys.argv[1])

    q = QuantumCircuit(2)
    q.h(0)
    q.cnot(0, 1)

    measures = [0,1]
    cbits = [0,1]
    q.measure(measures, cbits=cbits)

    task = Task()
    task.config(backend="ScQ-P18", shots=2000, compile=True)
    #task.load_account()

    #res = task.send(q, wait=False, name="zhaoyilun-test", group=GROUP_NAME)
    #group_res = task.retrieve_group(GROUP_NAME)
    #print(group_res)
    res = task.send(q, wait=False)
    print(res)
