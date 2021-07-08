#!/usr/bin/env python3
import sys
import json
from tqdm import tqdm
from pprint import pprint

assert len(sys.argv)>2, "too few arguments"
lines = open(sys.argv[1], 'r').readlines()
f = open(sys.argv[2], "w")
for i in tqdm(range(0, len(lines), 5)):
    id = int(lines[i])
    sent1 = lines[i+1].strip().strip("\n")
    sent2 = lines[i+2].strip().strip("\n")
    label = lines[i+3].strip().strip("\n")
    d = {"SNLI_ID":id, "PREMISE":sent1, "HYPOTHESIS":sent2, "LABEL":label}
    f.write(json.dumps(d)+"\n")
    # pprint(d)