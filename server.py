import sys
import json
import pandas as pd
from backend.models import User
# from flask_simple_captcha import CAPTCHA
from flask import Flask, render_template, request, jsonify
from backend.utils import rand_str, smart_int, read_data


# CAPTCHA_CONFIG = {'SECRET_CSRF_KEY':rand_str(length=43)}
app=Flask(__name__, static_url_path='/static')
# CAPTCHA=CAPTCHA(config=config.CAPTCHA_CONFIG)
# app=CAPTCHA.init_app(app)
assert len(sys.argv)>1, "need to give filename of the json or csv"
ANNOTATIONS = {}
DATASET = read_data(sys.argv[1]) # global variable to store the dataset.


# APP functions
@app.route('/',methods=['GET','POST'])
def index():
    # return "Hello World"
    return render_template("index.html")

@app.route('/instructions', methods=['GET','POST'])
def instructions():
    return render_template("instructions.html")

@app.route('/thankyou',methods=['GET','POST'])
def thankyou():
    import pandas as pd
    global ANNOTATIONS

    for user in ANNOTATIONS:
        pd.DataFrame(ANNOTATIONS[user]).to_csv(f"data/{user}.csv", index=False)

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
        context["DATASET_LENGTH"] = 0

        return render_template("complete.html", **context)
    
    else:
        index -= 1
        record = DATASET[index]
        if record["NEXT_NUM"] == len(DATASET)+1:
            record["NEXT_NUM"] = -1
        record["PREV_NUM"] = max(record["PREV_NUM"], 1)
        record["USERNAME"] = username
        record["DATASET_LENGTH"] = len(DATASET)

        return render_template("template.html", **record)

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'GET':
        render_template('register.html')

    if request.method == 'POST':
        data = request.get_json(force=True)  # parse as JSON
        print(data)

        return 'Success', 200

@app.route('/save', methods=['POST'])
def save_annotation():
    global DATASET
    global ANNOTATIONS

    data = request.get_json(force=True)  # parse as JSON
    index = smart_int(data["id"])
    username = data["username"]
    DATASET[index]["username"] = username
    DATASET[index]["sentence1"] = data["sentence1"]
    DATASET[index]["sentence2"] = data["sentence2"]
    try:
        ANNOTATIONS[username].append(DATASET[index])
    except KeyError:
        ANNOTATIONS[username] = [DATASET[index]]

    return 'Success', 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', use_reloader=True, port=81, debug=True)