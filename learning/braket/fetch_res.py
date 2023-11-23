import sys
from braket.aws import AwsQuantumTask

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <task-arn>")
    sys.exit(1)

arn = sys.argv[1]
task = AwsQuantumTask(arn=arn)
state = task.state()
res = task.result()


print(f"state: {state}\n\n------Result------\n{res}")
