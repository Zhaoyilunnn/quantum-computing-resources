"""
Name: guppylang
Version: 0.21.6
"""

from guppylang import guppy
from guppylang.std.builtins import owned
from guppylang.std.quantum import cx, h, measure, qubit, x, z


@guppy
def teleport(src: qubit @ owned, tgt: qubit) -> None:
    """Teleports the state in `src` to `tgt`."""
    # Create ancilla and entangle it with src and tgt
    tmp = qubit()
    h(tmp)
    cx(tmp, tgt)
    cx(src, tmp)

    # Apply classical corrections
    h(src)
    if measure(src):
        z(tgt)
    if measure(tmp):
        x(tgt)


from guppylang.std.builtins import result


@guppy
def teleport_one_state() -> None:
    src = qubit()
    tgt = qubit()

    # Let's teleport the |1> state
    x(src)
    teleport(src, tgt)

    result("teleported", measure(tgt))


sim_result = teleport_one_state.emulator(n_qubits=3).stabilizer_sim().with_seed(2).run()
print(list(sim_result.results))
