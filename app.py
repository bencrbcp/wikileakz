import json
from flask import Flask, render_template, request
from wikinav import *
app = Flask(__name__)
app._static_folder = "static"

@app.route('/', methods=['GET', 'POST'])
def index():
    data = {}
    return render_template('index.html', data=data)

@app.route('/handle_data', methods=['GET', 'POST'])
def handle_data():
    data = {}
    start = request.form.get('start', '')
    print("START: ".format(start))
    start = '/' + start.split('/', 3)[3]
    print("START': ".format(start))
    end = request.form.get('end', '')
    end = '/' + end.split('/', 3)[3]
    print("END: ".format(end))
    print("END': ".format(end))
    data['start'] = start
    data['end'] = end
    # /wiki/
    if start[0:6] == "/wiki/":
        w = WikipediaNav(maxt=25)
        res = w.searchAllFast(start, end)
        data['res'] = res

    # BEGIN PARSING TO WRITE JSON FILE
    jsonDict = {}
    articleSet = set()
    jsonDict['nodes'] = []
    jsonDict['links'] = [] # 'links' here refers to edges in the graph, not website links
    resLen = len(data['res'])

    for i in range(resLen):
        innerArrLen = len(data['res'][i])
        for j in range(innerArrLen):
            articlePath = data['res'][i][j]

            articleName = articlePath.split('/')[2]
            if (articleName not in articleSet):
                articleSet.add(articleName)
                articleLink = "https://en.wikipedia.org"+ articlePath
                
                jsonDict['nodes'].append({
                    "id" : articleName,
                })

            if ((j+1) < innerArrLen):
                nextNodePath = data['res'][i][j+1]
                nextNodeName = nextNodePath.split('/')[2]
                if (nextNodeName not in articleSet):
                    articleSet.add(nextNodeName)
                    nextNodeLink = "https://en.wikipedia.org"+ nextNodePath
                    
                    jsonDict['nodes'].append({
                        "id" : nextNodeName
                    })
                jsonDict['links'].append({
                    "source" : articleName,
                    "target" : nextNodeName
                })

    json_object = json.dumps(jsonDict, indent = 4)
    with open('static/graph.json', 'w') as outfile:
        outfile.write(json_object)
  
    return render_template('index.html', data=data)



if (__name__ == "__main__"):
    app.run(debug=True)
