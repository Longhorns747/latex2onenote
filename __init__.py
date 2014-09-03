from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=['POST'])
def process_latex():
    latex_input = request.form['latex_input']
    f = open('static/latexFiles/latex.tex', 'w')
    f.write(latex_input)
    f.close()

    bashCommand = "htlatex latex.tex"
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, cwd='static/latexFiles')
    output = process.communicate()[0]

    f = open('static/latexFiles/latex.html')
    finalHTML = f.read()

    return finalHTML

if __name__ == "__main__":
    app.run(debug="true")
