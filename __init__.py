from flask import Flask, render_template, request, redirect
import requests, random, string
import os
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=['POST'])
def process_latex():
    latex_input = request.form['latex_input']
    accessToken = request.form['access_token']

    #Make a randomly generated directory for latex compilation
    staticFilepath = 'static/latexFiles/' + random.choice(string.letters) + random.choice(string.letters) + random.choice(string.letters) + '/'

    d = os.path.dirname(staticFilepath)
    if not os.path.exists(d):
        os.makedirs(d)

    #If directory already exists, throw an error
    else:
        return render_template("error.html")

    f = open(staticFilepath + '/latex.tex', 'w')
    f.write(latex_input)
    f.close()

    #Compile LaTeX
    bashCommand = "htlatex latex.tex"
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, cwd=staticFilepath)
    output = process.communicate()[0]

    f = open(staticFilepath + '/latex.html')
    finalHTML = f.read()

    #Form POST request to the OneNote API
    url = "https://www.onenote.com/api/v1.0/pages?sectionName=LaTeX_Notes"
    headers = {'Content-Type' : 'Text/html', 'Authorization' : 'Bearer ' + accessToken}
    r = requests.post(url, data=finalHTML, headers=headers)
    jsonResponse = r.json()

    link = jsonResponse['links']['oneNoteWebUrl']['href']
    import shutil
    shutil.rmtree(staticFilepath)

    return render_template("success.html", onenote_url=link)

@app.route('/latex_input', methods=['GET', 'POST'])
def microsoft_response():
    authCode = request.args.get('code')

    f = open('static/client_secret.cfg', 'r+')
    clientSecret = f.read()

    #Exchange authentication code for access token
    url = 'https://login.live.com/oauth20_token.srf'
    headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
    urlData = {'client_id' : '0000000044127D98', 'redirect_uri' : 'http://latex2onenote.cloudapp.net/latex_input', 'client_secret' : clientSecret, 'code' : authCode, 'grant_type' : 'authorization_code'}
    r = requests.post(url, data=urlData, headers=headers)
    jsonResponse = r.json()
    accessToken = jsonResponse['access_token']
    return render_template("latex_input.html", access_token=accessToken)

if __name__ == "__main__":
    app.run(debug="true")
