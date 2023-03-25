"""Converters that convert np.array to statevector objects of other frameworks"""


class BaseConverter:

    def __init__(self) -> None:
        pass

    def convert(self):
        pass


class QiskitConverter(BaseConverter):

    def __init__(self) -> None:
        super().__init__()
