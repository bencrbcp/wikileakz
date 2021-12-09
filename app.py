from flask import Flask, render_template, request

app = Flask(__name__)
app._static_folder = "static"

@app.route('/', methods=['GET', 'POST'])
def index():
    data = request.form['projectFilepath']
    print(data)
    return render_template('index.html')

if (__name__ == "__main__"):
    app.run(debug=True)
