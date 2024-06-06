# Steps

## 00

Some benchmarks can be tested using the same script

```bash
# Bell State
python test_quiets_compilation.py bell.qu bell_state

# BV algorithm
python test_quiets_compilation.py bernstein_vazirani.qu bernstein_vazirani

# GHZ state
python test_quiets_compilation.py ghz.qu GHZ_state

# Control Adder
python test_quiets_compilation.py test_ctrl_adder.qu test_ctrl_adder

# Grover's algorithm
python test_quiets_compilation.py grover.qu grover_2q

python test_quiets_compilation.py ../qututor/recursion_test/test_scalarize_alloc/alloc.qu test_entry
```

## 01

Some benchmarks require using separate scripts

```bash
# QFT  
python test_qft_quiets.py

# Shor's algorithm
python test_shor_quiets.py 

# Adder
python test_adder_quiets.py

# Classical tools
python test_classical_tools_quiets.py 
```

Among these above examples, QFT and Adder failed with following errors

1. QFT
```
input : 00
Error message from the compiler:
        error: Encounter a list declaration with an unknown size. compilation failed.

17:23:04 compile 44(ERROR): Error message from the compiler:
        error: Encounter a list declaration with an unknown size. compilation failed.

Traceback (most recent call last):
  File "/home/zhaoyilun/workspace/github/quantum-computing-resources/learning/quingo/benchmark_tests/test_qft_quiets.py", line 65, in <module>
    Test_QFT_BB().test_qft_bb()
  File "/home/zhaoyilun/workspace/github/quantum-computing-resources/learning/quingo/benchmark_tests/test_qft_quiets.py", line 52, in test_qft_bb
    fn = compile(task, params=(blist,), qasm_fn=f"test_qft_bb_{blist}.qi")
  File "/home/zhaoyilun/workspace/gitee/quingo-runtime/src/quingo/core/compile.py", line 47, in compile
    raise RuntimeError(
RuntimeError: failed to compile the Quingo source file: /home/zhaoyilun/workspace/gitee/quingo-tutorials/src/quingo/test_qft.qu
```

2. Adder (Similar error with QFT)

```
Exception in thread Thread-30 (add_or_sub):
Error message from the compiler:
        error: Encounter a list declaration with an unknown size. compilation failed.
Traceback (most recent call last):
    raise RuntimeError(

17:23:48 compile 44(ERROR): Error message from the compiler:
        error: Encounter a list declaration with an unknown size. compilation failed.
```

## 02

Some benchmarks already failed for generating QCIS instructions


```bash

# Controlled Multiplier
cd path/to/quingo-tutorials
python src/qututor/ctrl-mult/test_ctrl_mult.py 

# vqe
cp test_vqe_quiets.py path/to/quingo-tutorials/src/qututor/vqe/
cd path/to/quingo-tutorials
python src/qututor/vqe/test_vqe_quiets.py
```