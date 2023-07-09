pytest -s -k "TestOracle and test_oracle" tst/qvm/integration/qvm_test.py --qasm logs/qvm/integration/frp/eval_selection/benchmarks.lst --backend FakeBrooklyn --metric pst | tee logs/qvm/oracle/brooklyn/pst_native_oracle_results.txt

pytest -s -k "TestOracle and test_oracle" tst/qvm/integration/qvm_test.py --qasm logs/qvm/integration/frp/eval_selection/benchmarks.lst --backend FakeCairo --metric pst | tee logs/qvm/oracle/cairo/pst_native_oracle_results.txt

pytest -s -k "TestOracle and test_oracle" tst/qvm/integration/qvm_test.py --qasm logs/qvm/integration/frp/eval_selection/benchmarks.lst --backend FakeCairo --metric kl | tee logs/qvm/oracle/cairo/kl_native_oracle_results.txt

pytest -s -k "TestFrpOracle and test_oracle" tst/qvm/integration/qvm_test.py --qasm logs/qvm/integration/frp/eval_selection/benchmarks.lst --backend FakeCairo | tee logs/qvm/oracle/cairo/kl_frp_oracle_results.txt

pytest -s -k "TestFrpOracle and test_pst_oracle" tst/qvm/integration/qvm_test.py --qasm logs/qvm/integration/frp/eval_selection/benchmarks.lst --backend FakeCairo | tee logs/qvm/oracle/cairo/pst_frp_oracle_results.txt
