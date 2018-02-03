import random
import json

from flask import Flask, render_template, redirect
app = Flask(__name__)

@app.route('/<string:page_name>/')
def load_page(page_name):
  if page_name.endswith('json'):
    with open('leveldata/{}'.format(page_name), 'r') as f:
      data = json.load(f)
    return render_template('game.html',data=data,winmsg=random.choice(['Well done!', 'Good job!', 'Nice!']))

  else:
    return redirect('/')

@app.route('/')
def load_index():
  return render_template('index.html')

app.run(host='0.0.0.0')
