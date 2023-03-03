import numpy as np
from quafu import QuantumCircuit, Task, User

user = User()
user.save_apitoken("4DEH53vA_IxMSg_fyZ3grsJ4ew7Jn-itMS6bcPlJ7E9.Qf0UzM1QDNwgjNxojIwhXZiwSO2ITM6ICZpJye.9JiN1IzUIJiOicGbhJCLiQ1VKJiOiAXe0Jye")

if __name__ == '__main__':

    q = QuantumCircuit(2)
    q.h(0)
    q.cnot(0, 1)
    
    measures = [0,1]
    cbits = [0,1]
    q.measure(measures, cbits=cbits)
    
    task = Task()
    task.load_account()

    res = task.send(q)
    print(res.counts)
