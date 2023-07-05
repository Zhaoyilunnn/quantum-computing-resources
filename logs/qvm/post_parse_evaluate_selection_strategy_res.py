import sys
import ast
from qutils.misc import check_equiv_two_list


def get_dict(file_name):
    res_dict = {}
    with open(file_name, "r") as f:
        for line in f:
            items = line.strip().split("\t")
            b_name = items[0]
            b_vals = items[1:]
            res_dict[b_name] = b_vals
    return res_dict


def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <naive-brute_force> <naive-reversed>")
        sys.exit(1)

    naive_brute_force = sys.argv[1]
    naive_reversed = sys.argv[2]

    naive_brute_force_dict = get_dict(naive_brute_force)
    naive_reversed_dict = get_dict(naive_reversed)

    for b_name, b_vals in naive_brute_force_dict.items():
        if b_name in naive_reversed_dict:
            b_vals_naive_reversed = naive_reversed_dict[b_name]
            cu_list_brute_force = ast.literal_eval(b_vals[10])
            cu_list_naive_reverse = ast.literal_eval(b_vals_naive_reversed[9])
            if check_equiv_two_list(cu_list_brute_force, cu_list_naive_reverse):
                continue
            print("\t".join([b_name, b_vals[-1], b_vals_naive_reversed[-1]]))


if __name__ == "__main__":
    main()
