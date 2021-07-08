def rand_str(length=12):
    import random
    from string import digits, ascii_letters
    
    chars = digits+ascii_letters+'_'
    string = ""
    for i in range(length):
        string += random.choice(chars)
    
    return string

def smart_int(x):
    if x is None:
        return 0
    elif x == "":
        return 0
    else: 
        return int(x)

def db_escape(string):
    string = str(string)
    string = string.replace("'","''")
    string = string.replace('"','""')

    return string

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
        examples.append({"SENTENCE_NUM":i, 
                         "PREMISE":tmp['sentence1'], 
                         "HYPOTHESIS":tmp['sentence2'], 
                         "PREV_NUM":i-1, 
                         "NEXT_NUM":i+1,
                         "LABEL":tmp['LABEL'],
                         "ID":tmp["ID"]})
        i += 1

    return examples

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