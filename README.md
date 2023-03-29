# qcs
Research repo for Quantum Computer System

- sim-beta: C++ version of qdao
- qdao: https://www.overleaf.com/read/jxfbxtbgztbb
- qvm: https://www.overleaf.com/read/kfpqgwjyghdn

# How to start

```
pip install -r requirements.txt
```

To understand how `qvm` and `qdao` works, suggest to run pytest and debug into the code step by step

```
# QDAO
pytest -s --trace tst/qdao/engine.py
```

```
# QVM
pytest -s --trace tst/qvm/integration/bench_test.py
```
