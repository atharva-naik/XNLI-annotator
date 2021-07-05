#!/usr/bin/env python3
import sys
import json
from numpy import inexact
import pandas as pd
from passlib.hash import pbkdf2_sha256
from backend.models import User, UserTable
# from flask_simple_captcha import CAPTCHA
from backend.utils import rand_str, smart_int, read_data
from flask import Flask, render_template, request, jsonify, redirect, flash


# CAPTCHA_CONFIG = {'SECRET_CSRF_KEY':rand_str(length=43)}
app=Flask(__name__, static_url_path='/static')
# CAPTCHA=CAPTCHA(config=config.CAPTCHA_CONFIG)
# app=CAPTCHA.init_app(app)
users = UserTable("data/users.csv")
assert len(sys.argv)>1, "need to give filename of the json or csv"
DATASET = read_data(sys.argv[1]) # global variable to store the dataset.
USERNAME = ""

# APP functions
@app.route('/',methods=['GET','POST'])
def index():
    # return "Hello World"
    return render_template("index.html", USERS=users.all_usernames())

@app.route('/instructions', methods=['GET','POST'])
def instructions():
    return render_template("instructions.html")

@app.route('/thankyou',methods=['GET','POST'])
def thankyou():
    return render_template("thankyou.html")

@app.route('/complete', methods=['GET','POST'])
def complete():
    username = request.args.get('user', default="Anonymous", type=str)
    context = {}
    context["USERNAME"] = username 
    context["DATASET_LENGTH"] = 0

    return render_template("complete.html", **context)

@app.route('/dashboard', methods=['GET','POST'])
def dahsboard():
    global users
    global DATASET

    username = request.args.get('user', default="Anonymous", type=str)
    context = {}
    context["USERNAME"] = username
    context["NUM_USERS"] = len(users)
    user = users.get_user(username)
    all = DATASET
    data = user.annotations.to_dict("records")
    E = 0
    C = 0
    N = 0
    U = 0
    for i in range(len(all)):
    # for i in range(len(data)):
        if all[i]["LABEL"] == "entailment":
            E += 1
        elif all[i]["LABEL"] == "contradiction":
            C += 1
        elif all[i]["LABEL"] == "neutral":
            N += 1
        else:
            U += 1
        for j in ["EP","EH","CH","CP","UP","UH","NH","NP"]:
            all[i]["status"] = "pending"
            try:
                all[i][j] = data[i][j].replace("<SEP>","▉")[:-1]
                all[i]["status"] = "complete"
            except IndexError:
                all[i][j] = ""
    context["data"] = all
    context["NUM_SENTENCES"] = len(all)
    context["NUM_ANNOTATED"] = len(data)
    context["PERCENT_ANNOTATED"] = f"{100*len(data)/len(all)}%"
    context["INTERANNOTATOR_AGREEMENT"] = "NA"
    context["E"] = 100*E/len(all)
    context["C"] = 100*C/len(all)
    context["N"] = 100*N/len(all)
    context["U"] = 100*U/len(all)
    context["PERCENT_ANNOTATED_INT"] = 100*len(data)/len(all)
    return render_template("dashboard.html", **context)

@app.route('/annotate', methods=['GET','POST'])
def annotation_page():
    global users
    global DATASET
    id = request.args.get('id', default=1, type=int) 
    # 1 for the first sentence, 2 for the second ... N for the Nth, len(DATASET) for the last one.
    username = request.args.get('user', default="Anonymous", type=str)
    record = DATASET[id-1]
    record["NEXT_URL"] = f'/annotate?id={id+1}&user={username}'
    record["PREV_URL"] = f'/annotate?id={id-1}&user={username}'
    if id == len(DATASET):
        record["NEXT_URL"] = f'/complete?user={username}'
        print(record["NEXT_URL"])
    elif id == 1:
        record["PREV_URL"] = f'/annotate?id={id}&user={username}'
    user = users.get_user(username)
    record["USERNAME"] = username
    record["DATASET_LENGTH"] = len(DATASET)
    annotation = user.fetch_annotation(id)
    record.update(annotation)
    # print(record)
    return render_template("template.html", **record)

@app.route('/register', methods=['POST','GET'])
def register():
    global users
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form["password"]
        repeat_password = request.form["repeat_password"]
        if repeat_password != password:
            return render_template('invalid.html', PREVIOUS_URL="/register")
        # return 'Success', 200
        password = pbkdf2_sha256.hash(password)
        users.add_user({"username":username, 
                        "email":email,
                        "password":password})
        print(username, email, password, repeat_password)
        users.save()

        return redirect(f'/annotate?id=1&user={username}')

@app.route('/login', methods=['POST','GET'])
def login():
    global users
    global USERNAME
    if request.method == 'GET':
        USERNAME = request.args.get('user')

        return render_template('login.html', USERNAME=USERNAME)

    if request.method == 'POST':
        password = request.form["password"]
        user = users.get_user(USERNAME)
        print(user)
        if user.authenticate(password):
            return redirect(f'/annotate?id=1&user={USERNAME}')
        else: 
            return redirect(f'/login?user={USERNAME}')

@app.route('/save', methods=['POST'])
def save_annotation():
    global users
    global DATASET

    data = request.get_json(force=True)  # parse as JSON
    data["id"] = smart_int(data["id"])
    username = data["username"]
    user = users.get_user(username)
    if id not in user.ids:
        print("record doesn't exist, so adding it")
        user.add_annotation(data)
    else:
        print("updating record")
        user.update_annotation(id=data["id"], annotation=data)
    user.save()
    # DATASET[index]["username"] = username
    # DATASET[index]["sentence1"] = data["sentence1"]
    # DATASET[index]["sentence2"] = data["sentence2"]

    # try:
    #     ANNOTATIONS[username].append(DATASET[index])
    # except KeyError:
    #     ANNOTATIONS[username] = [DATASET[index]]
    return 'Success', 200


if __name__ == "__main__":
    # config for local testing:
    app.run(host='0.0.0.0', use_reloader=True, port=81, debug=True)
    # config for manga server:
    # app.run(host='0.0.0.0', use_reloader=True, port=11200, debug=True)
