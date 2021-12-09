from flask import Flask, render_template, request

app = Flask(__name__)
app._static_folder = "static"

@app.route('/', methods=['GET', 'POST'])
def index():
    data = {}
    data2 = request.form.get('projectFilepath', '')
    data['penis'] = str(data2)
    return render_template('index.html', data=data)

if (__name__ == "__main__"):
    app.run(debug=True)
