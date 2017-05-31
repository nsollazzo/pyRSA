'''
start.py
@author: Salvatore Giammanco
@version: 1.0
@date: March 16th 2017
'''

from flask import Flask, render_template, request

from RSA import RSA

app = Flask(__name__)

rsa = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    about = "Designed and developed by Giammanco and Sollazzo"
    return render_template("index.html", page="about", about=about)


@app.route("/generate")
def generate():
    global rsa
    rsa = RSA()
    step_list = rsa.dict()
    return render_template("index.html", page="generate", step_list=step_list)


@app.route("/encrypt", methods=['POST'])
def encrypt():
    global rsa
    tmp = rsa.encrypt(request.form['plain'])
    stri = ""
    for element in range(len(tmp)):
        stri += str(tmp[element])
        if element != len(tmp) - 1:
            stri += "-"
    return stri
    # return ''.join(stri+=str(str(tmp[element])+"-")[:-1] for element in range(len(tmp)))


@app.route("/decrypt", methods=['POST'])
def decrypt():
    global rsa

    tmp = request.form['encrypted'].split("-")
    tmp = [int(element) for element in tmp]
    print(tmp)
    tmp = rsa.decrypt(tmp)

    return tmp


if __name__ == "__main__":
    app.run()
