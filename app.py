from flask import Flask, render_template, request, redirect, url_for,flash
from pymongo import MongoClient
import string
from  random import choice
import validators

cluster=MongoClient("mongodb+srv://udaykiran:udaykiran123@cluster0.p4c6kcv.mongodb.net/?retryWrites=true&w=majority")

db=cluster["url-shorten"]
collection=db["history"]
app=Flask(__name__)

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route('/homepage')
def homepage():
    return render_template("homepage.html")

@app.route('/r/<key>')
def r(key):
    res=collection.find_one({'short-val':key})
    org_url=res['original-url']
    return redirect(org_url)

    
@app.route('/retrieve',methods=["POST","GET"])
def retrieve():
    a=request.form.get("url")
    if validators.url(a):
        sh_v=collection.find()
        if collection.find_one({'original-url':a}):
            res=collection.find_one({'original-url':a})
            short_url=res['short-url']
            return render_template("homepage.html",shorted=short_url,org_url=a)
        else:
            cur=collection.find({})
            k=[]
            for i in cur:
                k.append(i['short-val'])
            while True:
                sv=short(6)
                if sv not in k:
                    short_url=request.host_url+"r/"+sv
                    details={'original-url':a,'short-url':short_url,'short-val':sv}
                    collection.insert_one(details)
                    return render_template("homepage.html",shorted=short_url,org_url=a)
    else:
        return render_template("homepage.html",msg="Enter valid URL!")


def short(n):
    return ''.join(choice(string.ascii_letters+string.digits) for i in range(n))

@app.route("/history")
def history():
    cur=collection.find({})
    k={}
    for i in cur:
        k[i['original-url']]=i['short-url']
    return render_template("history.html",k=k)
      


if __name__=='__main__':
    app.run(debug=True)
