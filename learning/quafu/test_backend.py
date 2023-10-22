import json
from typing import Any
from matplotlib.pyplot import Figure
from quafu.tasks.tasks import Task
from quafu.users.userapi import User


class QuafuBackendJsonEncoder(json.JSONEncoder):
    """Transform qiskit backendconfiguration/properties to json"""

    def default(self, o: Any) -> Any:
        if isinstance(o, Figure):
            return "A matplotlib figure"
        elif isinstance(o, complex):
            return str(o.real) + str(o.imag) + "j"
        else:
            return super().default(o)


user = User()
user.get_backends_info()
backends = user.get_available_backends()
chip_info = backends["ScQ-P10"].get_chip_info()
chip_info = backends["ScQ-P136"].get_chip_info()
json_str = json.dumps(chip_info["full_info"], indent=4)
json_str = json.dumps(chip_info, indent=4, cls=QuafuBackendJsonEncoder)
print(json_str)
