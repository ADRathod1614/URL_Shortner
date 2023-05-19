from flask import Flask,render_template,redirect,request
import random
import string
import json

app= Flask(__name__)
Short={}

def generate_short_url(length=6):
    chars=string.ascii_letters+string.digits
    short_url="".join(random.choice(chars) for _ in range(length))
    return short_url

@app.route('/',methods=["GET","POST"])
def index():
    if request.method=="POST":
        long_url=request.form['long_url']
        short_url= generate_short_url()
        while short_url in Short:
            short_url=generate_short_url()

        Short[short_url]=long_url
        with open("urls.json","w") as f:
            json.dump(Short,f)
        return f"shortened URL {request.url_root}{short_url}"
    return render_template("index.html")

@app.route('/<short_url>')
def redirect_url(short_url):
    loop_url=Short.get(short_url)
    if loop_url:
        return redirect(loop_url)
    else:
        return "URL NOT FOUND",404

if __name__=="__main__":
    with open('urls.json',"r") as f:
        Short=json.load(f)
    app.run(debug=True)

