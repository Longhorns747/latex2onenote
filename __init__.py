from flask import Flask, render_template, request, redirect, session
import requests, random, string
import os
app = Flask(__name__)

@app.route("/")
def home():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                  for x in xrange(32))
    session['state'] = state
    return render_template("index.html", state=state)

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

@app.route("/process", methods=['POST'])
def process_latex():
    if request.args.get('state', '') != session['state']:
        return render_template("error.html", message="Hmmm, the state seems to be off here!")

    latex_input = request.form['latex_input']
    accessToken = request.form['access_token']

    #Make a randomly generated directory for latex compilation
    staticFilepath = 'static/latexFiles/' + random.choice(string.letters) + random.choice(string.letters) + random.choice(string.letters) + '/'

    d = os.path.dirname(staticFilepath)
    if not os.path.exists(d):
        os.makedirs(d)

    #If directory already exists, throw an error
    else:
        return render_template("error.html", message="Oh no D:! Something went wrong :( Please try again!")

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

app.secret_key = open('static/app_key.cfg', 'r+').read()
if __name__ == "__main__":
    app.run(debug="true")
