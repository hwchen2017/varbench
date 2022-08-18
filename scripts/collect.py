#!/usr/bin/env python3

import os
import re
from math import isnan, nan

from natsort import natsort_key
from tabulate import tabulate
from unidecode import unidecode

root = "../"
ham_types = ["TfIsing", "Heisenberg", "J1J2", "Hubbard"]


def split_cols(s):
    cols = s.strip().strip("|").split("|")
    cols = [x.strip() for x in cols]
    return cols


def parse_float(s):
    # Sometimes there are special Unicode characters, so we normalize them
    s0 = s
    s = unidecode(s0)
    if s != s0:
        print(f"Special character detected in {s0}")

    s = s.replace("(", "").replace(")", "")
    if not s:
        return 0

    try:
        return float(s)
    except ValueError:
        print(f"Failed to parse float {s}")
        return nan


def parse_file(data, file_path, ham_attr):
    fields = ["method", "energy", "energy variance"]

    state = 0
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if state == 0:
                line = line.lower()
                if not all(x in line for x in fields):
                    continue

                cols = split_cols(line)
                field_indices = {x: cols.index(x) for x in fields}
                state = 1

            elif state == 1:
                if "---" in line:
                    continue

                cols = split_cols(line)

                def warn(msg):
                    print(f"Warning: {msg}: {ham_attr + tuple(cols)}")

                method = cols[field_indices["method"]]

                energy = cols[field_indices["energy"]]
                energy = parse_float(energy)
                if isnan(energy):
                    warn("Failed to parse energy")
                    continue
                if energy == 0:
                    warn("Zero energy")
                    continue
                if energy > 0:
                    warn("Positive energy")
                    # energy *= -1

                energy_var = cols[field_indices["energy variance"]]
                energy_var = parse_float(energy_var)
                if isnan(energy_var):
                    warn("Failed to parse variance")
                    # continue
                if energy_var == 0:
                    # warn("Zero variance")
                    # continue
                    pass
                if energy_var < 0:
                    warn("Negative variance")
                    # continue

                data.append(ham_attr + (method, energy, energy_var))

            else:
                raise ValueError(f"Unknown state: {state}")


# (ham_type, ham_param, method, energy, energy_var)
def get_data():
    data = []
    for _dir in os.scandir(root):
        if _dir.name not in ham_types:
            continue
        ham_type = _dir.name

        for file in os.scandir(_dir):
            if not file.is_file() or file.name == "README.md":
                continue
            ham_param = file.name.replace(".md", "")

            file_path = os.path.join(root, _dir.name, file.name)
            parse_file(data, file_path, (ham_type, ham_param))

    return data


def get_ham_idx(ham_type):
    return ham_types.index(ham_type)


def data_key(row):
    return get_ham_idx(row[0]), natsort_key(row[1:])


def get_ndof(ham_attr):
    ham_type, ham_param = ham_attr
    if ham_type == "Hubbard":
        pattern = r"[OP]_(\d+)_(\d+)"
    else:
        pattern = r"[OP]_(\d+)"
    match = re.compile(pattern).search(ham_param)
    if not match:
        print(f"Warning: Failed to parse #DOF: {ham_attr}")
        return nan

    try:
        if ham_type == "Hubbard":
            ndof = int(match.group(1)) + int(match.group(2))
        else:
            ndof = int(match.group(1))
    except ValueError:
        print(f"Warning: Failed to parse #DOF: {ham_attr}")
        return nan

    return ndof


def filter_energy_var(data):
    out = []
    for row in data:
        if row[4] > 0:
            out.append(row)
    return out


def main():
    data = get_data()
    data.sort(key=data_key)
    print(tabulate(data, tablefmt="plain"))


if __name__ == "__main__":
    main()
