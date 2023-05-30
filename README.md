# qcs
Research repo for Quantum Computer System

- sim-beta: C++ version of qdao
- qdao: https://www.overleaf.com/read/jxfbxtbgztbb
- qvm: https://www.overleaf.com/read/kfpqgwjyghdn

# How to start

## Install QDAO
```SHELL
git clone https://github.com/Zhaoyilunnn/qdao.git
cd qdao
python setup.py install
cd -
```

## Install PyQuafu

Currently we use dev branch, see [pr11](https://github.com/ScQ-Cloud/pyquafu/pull/11)

```SHELL
git clone https://github.com/ScQ-Cloud/pyquafu.git
cd pyquafu
git checkout dev
pip install -r requirements.txt
python setup.py install
cd -
```

## Install dependencies
```SHELL
git clone https://github.com/Zhaoyilunnn/qcs.git
cd qcs
pip install -r requirements.txt
```

## Run QDAO tests

- `<qasm-name>` are file names in [benchmarks](https://github.com/Zhaoyilunnn/qcs/tree/master/qdao/benchmarks/qasm) directory, name format: `<app>_<# qubits>_<suffix>.qasm`.
- `<# qubits>` is the number of qubits, see benchmark name.
- `<m>` is the number of qubits in a compute unit, see the [paper](https://www.overleaf.com/read/jwhwvkgngmfd).
- `<t>` is the number of qubits in a storage unit.

```SHELL
pytest -s -k test_run_quafu_any_qasm tst/qdao/engine.py --qasm <qasm-name> --nq <# qubits> --np <m> --nl <t>

# Example
pytest -s -k test_run_quafu_any_qasm tst/qdao/engine.py --qasm random_12_9_max_operands_2_gen.qasm --nq 12
```

## TBD
To understand how `qvm` and `qdao` works, suggest to run pytest and debug into the code step by step

```
# QDAO
pytest -s --trace tst/qdao/engine.py
```

```
# QVM
pytest -s --trace tst/qvm/integration/bench_test.py
```
