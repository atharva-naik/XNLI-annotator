#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union, Dict, List

def write_jsonl(data: list, path: str) -> int:
    """write a list of homogenous (same key dictionaries) to a .jsonl file.

    Args:
        data (list): list of dictionaries data.
        path (str): path to JSONL file.

    Returns:
        int: number of bytes written
    """
    import json
    num_bytes = 0
    with open(path, "w") as f:
        for rec in data:
            num_bytes += f.write(json.dumps(rec)+"\n")

    return num_bytes

def format_data(data: List[dict], mapping: dict) -> List[dict]:
    mapped_data = []
    for rec in data:
        new_rec = {}
        for key, new_key in mapping.items():
            new_rec[new_key] = rec[key]
        mapped_data.append(new_rec)
    
    return mapped_data

def read_jsonl(path: str):
    import json
    data = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            data.append(json.loads(line))

    return data


if __name__ == "__main__":
    import sys
    import pathlib

    path = sys.argv[1]
    path_obj = pathlib.Path(path)
    data = read_jsonl(path)
    data = format_data(
        data, {
        "id": "SNLI_ID",
        "sentence1": "PREMISE",
        "sentence2": "HYPOTHESIS",
        "label": "LABEL",
    })
    # print(data[:10])
    path_proc = path_obj.parent / (path_obj.stem + "_formatted" + path_obj.suffix)
    # print(path_proc)
    print(write_jsonl(data, path_proc))