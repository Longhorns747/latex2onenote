from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    bashCommand = "echo 'Hello World!'"
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(debug="true")
