from quafu.tasks.tasks import Task
from quafu.users.userapi import User

user = User()
user.get_backends_info()
backends = user.get_available_backends()
chip_info = backends['ScQ-P10'].get_chip_info()
