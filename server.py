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

@app.route('/annotate', methods=['GET','POST'])
def annotation_page():
    global users
    global DATASET
    index = request.args.get('id', default=1, type=int)
    username = request.args.get('user', default="Anonymous", type=str)
    
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
        user = users.get_user(username)
        annotation = user.fetch_annotation(id=index+1)
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
    if user.fetch_annotation(id=data["id"]) == "":
        user.add_annotation(data)
    else:
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
    app.run(host='0.0.0.0', use_reloader=True, port=11200, debug=True)
