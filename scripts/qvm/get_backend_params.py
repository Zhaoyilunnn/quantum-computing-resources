from datetime import date, datetime
import os
import sys

from qiskit import IBMQ
from qvm.util.backend import BackendAdjMatGraphExtractor


#IBMQ.save_account("036d2bca315b21dc9525cd05217943de9eab08326f37d652ac23aed075ea3e32ea3a983602b728e1b7c3e5e2a157959dcd0b834eb34ce607b3ec1d6401e9594d", overwrite=True)
DEVICE_LIST = ['ibm_oslo', 'ibmq_manila', 'ibm_nairobi', 'ibmq_quito', 'ibmq_belem', 'ibmq_lima']
provider = IBMQ.load_account()


#backend = provider.get_backend('ibmq_manila')
backend_list = provider.backends()
#backend = provider.get_backend('ibmq_kolkata')
#print(backend.status().pending_jobs)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <log-path>")
        sys.exit(1)

    log_dir = sys.argv[1]
    log_name = date.isoformat(datetime.now()) + '.log'
    file_path = os.path.join(log_dir, log_name)

    with open(file_path, 'w') as f:
        for backend in backend_list:
            extractor = BackendAdjMatGraphExtractor(backend)
            b_name = backend.name()
            try:
                err_map = extractor.extract()
                for i, err_i in enumerate(err_map):
                    for j, err_ij in enumerate(err_i):
                        f.write(f"{b_name}\t{i}-{j}\t{err_ij}\n")
                rd_err = extractor.get_readout_errs()
                for i, rd_i in enumerate(rd_err):
                    f.write(f"{b_name}\t{i}\t{rd_i}\n")
            except Exception:
                continue
