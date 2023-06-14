import json
from quafu.tasks.tasks import Task
from quafu.users.userapi import User

user = User()
user.get_backends_info()
backends = user.get_available_backends()
chip_info = backends['ScQ-P10'].get_chip_info()
json_str = json.dumps(chip_info["full_info"], indent=4)
print(json_str)
