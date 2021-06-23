import os
import sys
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path

assert len(sys.argv) > 1, "need to give file name as input."
data = pd.read_csv(sys.argv[1]).to_dict("records")
proc_data = []
for record in data:
    soup1 = BeautifulSoup(record["sentence1"])
    soup2 = BeautifulSoup(record["sentence2"])
    text1 = soup1.text.strip()
    text2 = soup2.text.strip()
    
filename = os.path.splitext(sys.argv[1])[0]+"_proc.csv"
pd.DataFrame(proc_data).to_csv(filename)

def compare(x,y,tol=1e-8):
    import math 
    matches = 0

    for i,j in zip(x,y):
        if abs(i-j) < 1e-8:
            matches += 1

    return matches

# add-apt-repository ppa:inkscape.dev/stable
# apt update
# apt install inkscape
