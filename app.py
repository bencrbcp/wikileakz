from flask import Flask, render_template, request
from wikinav import *
app = Flask(__name__)
app._static_folder = "static"

@app.route('/', methods=['GET', 'POST'])
def index():
    data = {}
    start = request.form.get('start', '')
    end = request.form.get('end', '')
    data['start'] = start
    data['end'] = end
    # /wiki/
    if start[0:6] == "/wiki/":
        w = WikipediaNav(maxt=25)
        res = w.searchAllFast(start, end)
        data['res'] = res
    return render_template('index.html', data=data)

if (__name__ == "__main__"):
    app.run(debug=True)
