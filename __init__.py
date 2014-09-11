from flask import Flask, render_template, request, redirect
import os
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=['POST'])
def process_latex():
    latex_input = request.form['latex_input']
    staticFilepath = 'static/latexFiles'

    d = os.path.dirname(staticFilepath)
    if not os.path.exists(d):
        os.makedirs(d)

    f = open(staticFilepath + '/latex.tex', 'w')
    f.write(latex_input)
    f.close()

    bashCommand = "htlatex latex.tex"
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, cwd=staticFilepath)
    output = process.communicate()[0]

    f = open(staticFilepath + '/latex.html')
    finalHTML = f.read()

    return finalHTML

@app.route('/latex_input', methods=['GET', 'POST'])
def microsoft_response():
    authCode = request.args.get('code')

    f = open('static/client_secret.cfg', 'r+')
    clientSecret = f.read()

    url = 'https://login.live.com/oauth20_token.srf'
    headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
    urlData = {'client_id' : '0000000044127D98', 'redirect_uri' : 'http://latex2onenote.cloudapp.net/latex_input', 'client_secret' : clientSecret, 'code' : authCode, 'grant_type' : 'authorization_code'}
    r = requests.post(url, data=urlData, headers=headers)
    jsonResponse = r.json()
    accessToken = jsonResponse['access_token']
    return render_template("latex_input.html", access_token=accessToken)

if __name__ == "__main__":
    app.run(debug="true")
