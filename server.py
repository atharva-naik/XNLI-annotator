import sys
import json
import pandas as pd
from flask import Flask, render_template, request, jsonify

app=Flask(__name__)
assert len(sys.argv)>1, "need to give filename of the json or csv"

# Utility functions
def rand_str(length=16):
    import random
    from string import ascii_letters, digits
    
    op_str = ""
    population = ascii_letters + digits
    for i in range(length):
        op_str += random.sample(population, 1)[0]

    return op_str

def read_data(path):
    import json
    from tqdm import tqdm
    
    '''To load list of dictionaries from jsonl file.'''
    i = 1
    examples = []
    with open(path) as f:
        lines = f.readlines()
    for line in tqdm(lines, desc="reading json"):
        tmp = json.loads(line)
        examples.append({"SENTENCE_NUM":i, "PREMISE":tmp['sentence1'], "HYPOTHESIS":tmp['sentence2'], "PREV_NUM":i-1, "NEXT_NUM":i+1})
        i += 1

    return examples

DATASET = read_data(sys.argv[1]) # global variable to store the dataset.

def fill_template(html_template, **kwargs):
    import os
    import random
    
    assert isinstance(html_template, str), "the html template should be the file path."
    os.makedirs("./templates/tmp", exist_ok=True)
    html_template = open(html_template, "r")
    for KEYWORD in kwargs:
        html_template = html_template.replace(KEYWORD, kwargs[KEYWORD])    
    op_str = rand_str()
    fname = f"./templates/tmp/{op_str}.html" 
    open(fname, "w").write(html_template)

    return f"tmp/{op_str}.html"

# APP functions
@app.route('/',methods=['GET','POST'])
def index():
    # return "Hello World"
    return render_template("index.html")

@app.route('/thankyou',methods=['GET','POST'])
def thankyou():
    # return "Hello World"
    return render_template("thankyou.html")

@app.route('/annotate', methods=['GET','POST'])
def annotation_page():
    global DATASET
    index = request.args.get('id', default=1, type=int)
    username = request.args.get('user', default="Anonymous", type=str)
    print(username)
    print(index)
    
    if index == -1:
        context = {}
        context["USERNAME"] = username 
        return render_template("complete.html", **context)
    
    else:
        index -= 1
        record = DATASET[index]
        if record["NEXT_NUM"] == len(DATASET)+1:
            record["NEXT_NUM"] = -1
        record["PREV_NUM"] = max(record["PREV_NUM"], 1)
        record["USERNAME"] = username

        return render_template("template.html", **record)

@app.route('/save', methods=['GET', 'POST'])
def save_annotation():
    # GET request
    if request.method == 'GET':
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'Success', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)