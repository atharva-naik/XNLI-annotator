import sys
import json
import pandas as pd
from flask import Flask, render_template

app=Flask(__name__)
assert len(sys.argv)>1, "need to give filename of the json or csv"
data = sys.argv[1]

# Utility functions
def read_data(path):
    

# APP functions
@app.route('/',methods=['GET','POST'])
def index():
    # return "Hello World"
    return render_template("index.html")

def 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)