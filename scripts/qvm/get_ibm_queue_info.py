from datetime import date, datetime
import os
import sys

from qiskit import IBMQ


#IBMQ.save_account("036d2bca315b21dc9525cd05217943de9eab08326f37d652ac23aed075ea3e32ea3a983602b728e1b7c3e5e2a157959dcd0b834eb34ce607b3ec1d6401e9594d", overwrite=True)
DEVICE_LIST = ['ibm_oslo', 'ibmq_manila', 'ibm_nairobi', 'ibmq_quito', 'ibmq_belem', 'ibmq_lima']
provider = IBMQ.load_account()


#backend = provider.get_backend('ibmq_manila')
backend_list = provider.backends()
#backend = provider.get_backend('ibmq_kolkata')
#print(backend.status().pending_jobs)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <log-dir-path>")
        sys.exit(1)
    log_dir = sys.argv[1]
    log_name = date.isoformat(datetime.now()) + '.log'
    file_path = os.path.join(log_dir, log_name)

    with open(file_path, 'w') as f:
        for backend in backend_list:
            f.write(f"{backend.name()}\t{backend.status().pending_jobs}\n")
