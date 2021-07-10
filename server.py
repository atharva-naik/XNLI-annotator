#!/usr/bin/env python3
import sys
import json
import math
import time
import pandas as pd
from datetime import datetime
from backend.database import Database
from passlib.hash import pbkdf2_sha256
from backend.utils import rand_str, smart_int, COLOR_MAP
from flask import Flask, g, render_template, request, jsonify, redirect, flash, send_file


# assert len(sys.argv)>1, "need to give filename of the json or csv"
app = Flask(__name__, static_url_path='/static')
db = Database("data.sqlite")
db.dropTable("sentences")
size = db.addTableFromJSONL("sentences",
            path="data/SNLI_sample.jsonl")
db.close()
USERNAME = ""

# DATABASE close when app crashes:
@app.teardown_appcontext
def close(error):
    # db.close()
    pass

# APP endpoints:
@app.route('/',methods=['GET','POST'])
def index():
    db = Database("data.sqlite")
    db.addTable("users", 
                id="INTEGER PRIMARY KEY AUTOINCREMENT", 
                username="text NOT NULL UNIQUE",
                email="text",
                password="text")
    USERS = db.allTableColumns("users").get("username",[])
    db.close()

    return render_template("index.html", USERS=USERS)

@app.route('/instructions', methods=['GET','POST'])
def instructions():
    return render_template("instructions.html")

@app.route('/thankyou',methods=['GET','POST'])
def thankyou():
    return render_template("thankyou.html")

@app.route('/complete', methods=['GET','POST'])
def complete():
    USERNAME = request.args.get('user', default="Anonymous", type=str)

    return render_template("complete.html", USERNAME=USERNAME)

@app.route('/dashboard', methods=['GET','POST'])
def dahsboard():
    E,C,N,U = 0,0,0,0
    context = {}
    db = Database("data.sqlite")
    context["USERNAME"] = request.args.get('user', default="Anonymous", type=str)
    context["NUM_USERS"] = len(db.table_names)-3
    sentences = db.allTableRows("sentences")
    for i in range(size):
        if sentences[i]["LABEL"] == "entailment":
            E += 1
        elif sentences[i]["LABEL"] == "contradiction":
            C += 1
        elif sentences[i]["LABEL"] == "neutral":
            N += 1
        else:
            U += 1
        # for j in ["EP","EH","CH","CP","UP","UH","NH","NP"]:
        # sentences[i]["status"] = "pending"
        record = db.getTableRow(context["USERNAME"], page_no=i+1)
        sentences[i].update(record)
        if record == {}:
            sentences[i]["status"] = "pending"
        else:
            sentences[i]["status"] = "complete"
        
    context["data"] = sentences
    context["NUM_SENTENCES"] = len(sentences)
    context["NUM_ANNOTATED"] = db.getTableLength(context["USERNAME"])
    # context["PERCENT_ANNOTATED"] = f"{100*db.getTableLength(context['USERNAME'])/len(sentences)}%"
    context["INTERANNOTATOR_AGREEMENT"] = "NA"
    context["E"] = 100*E/len(sentences)
    context["C"] = 100*C/len(sentences)
    context["N"] = 100*N/len(sentences)
    context["U"] = 100*U/len(sentences)
    context["PERCENT_ANNOTATED_INT"] = 100*db.getTableLength(context['USERNAME'])/len(sentences)
    db.close()

    return render_template("dashboard.html", **context)

@app.route('/annotate', methods=['GET','POST'])
def annotation_page():
    id = request.args.get('id', default=1, type=int) # 1 for the first sentence, 2 for the second ... N for the Nth, len(DATASET) for the last one.
    username = request.args.get('user', default="Anonymous", type=str)
    db = Database("data.sqlite")
    db.addTable(username, 
                id="INTEGER PRIMARY KEY AUTOINCREMENT", 
                page_no="text NOT NULL UNIQUE",
                snli_id="text NOT NULL UNIQUE",
                EP="text",
                CP="text",
                NP="text",
                UP="text",
                EH="text",
                CH="text",
                NH="text",
                UH="text")
    record = db.getTableRow("sentences", id=id)
    annotation = db.getTableRow(username, page_no=id)
    db.close()
    record["NEXT_URL"] = f'/annotate?id={min(id+1,size)}&user={username}'
    record["PREV_URL"] = f'/annotate?id={max(id-1,1)}&user={username}'
    record["PAGE_NUM"] = id
    record["COLOR"] = COLOR_MAP.get(record["LABEL"])
    record.update(annotation)
    record["USERNAME"] = username
    print(record)

    return render_template("template.html", **record)

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        repeat_password = request.form["repeat_password"]
        if repeat_password != password:
            return render_template('invalid.html', PREVIOUS_URL="/register")
        db = Database("data.sqlite")
        db.addTableRow("users",
                       username=request.form['username'],
                       email=request.form['email'],
                       password=pbkdf2_sha256.hash(password))
        db.close()

        return redirect(f'/annotate?id=1&user={username}')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        USERNAME = request.args.get('user')
        print("username", USERNAME)

        return render_template('login.html', USERNAME=USERNAME)

    if request.method == 'POST':    
        USERNAME = request.args.get('user')
        password = request.form["password"]
        print("username", USERNAME)
        db = Database("data.sqlite")
        record = db.getTableRow("users", username=USERNAME)
        print(record["password"])
        db.close()
        if pbkdf2_sha256.verify(password, record["password"]):
            return redirect(f'/annotate?id=1&user={USERNAME}')
        else: 
            return redirect(f'/login?user={USERNAME}')

@app.route('/export')
def export():
    username = request.args.get('user')
    print(f"csv export requested by: {username}")
    db = Database("data.sqlite")
    now = int(time.time())
    filename = "exports/"+f"{username}_{now}.jsonl"
    db.toJSONL(username, filename)
    db.close()

    return send_file(filename, 
                     cache_timeout=1,
                     attachment_filename=f"{username}.jsonl",
                     as_attachment=True)

@app.route('/save', methods=['POST'])
def save_annotation():
    data = request.get_json(force=True)  # parse as JSON
    username = data["username"]
    db = Database("data.sqlite")
    record = db.getTableRow("sentences", id=data["id"])
    data["SNLI_ID"] = record["SNLI_ID"]
    data["PAGE_NO"] = data["id"]
    del data["id"]
    del data["username"]
    db.modifyTableRow(username,
                      "page_no",
                      data["PAGE_NO"],
                      **data) 
    db.close()

    return 'Success', 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', use_reloader=True, port=11200, debug=True)
