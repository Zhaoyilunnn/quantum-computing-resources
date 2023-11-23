"""
amazon-braket-default-simulator 1.20.1
amazon-braket-schemas           1.19.1.post0
amazon-braket-sdk               1.62.1
"""



import boto3
from braket.aws import AwsDevice
from braket.circuits import Circuit
from braket.devices import LocalSimulator

# device = AwsDevice("arn:aws:braket:::device/quantum-simulator/amazon/sv1")
device = LocalSimulator()

bell = Circuit().h(0).cnot(0, 1)
task = device.run(bell, shots=100)
print(task.result().measurement_counts)
