from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return open("index.html").read()

@app.route('/<path:website>', methods=['GET'])
def anyget(website):
    output = requests.get(f"https://{website}").text
    output = output.replace("\"/",f'"/{website}/').replace("https://",f"/").replace("http://",f"/")
    return output

app.run()