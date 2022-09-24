for q in 20 22 24 26 28; do ./bin/simulator -qobj_file ../test/data/unitary_random_${q}_inst.json -nq ${q} -np $((q-2)) -nl $((q-4)) | tee random.$q.log; done
