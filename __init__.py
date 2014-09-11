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

if __name__ == "__main__":
    app.run(debug="true")
