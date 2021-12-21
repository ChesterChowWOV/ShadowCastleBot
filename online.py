from flask import Flask
from threading import Thread

app = Flask("app")

@app.route('/')
def home():
  return "Online"
  
def run():
  app.run(host='0.0.0.0',port=8080)

def start():
  t = Thread(target=run)
  t.start()