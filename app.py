from flask import Flask, request
import json
import time
app = Flask(__name__)

@app.route('/wifi', methods=['POST'])
def add_profiles():
    timestamp  = time.time()
    with open('profiles.json', 'r+') as f:
        data = json.load(f)
        data.append({'Data':request.json, "Time": timestamp })
        f.seek(0)
        json.dump(data, f)
    return 'Profiles adicionados com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)
