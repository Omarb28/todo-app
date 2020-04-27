from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html', data=[
    {'description': 'Todo 1'},
    {'description': 'Todo 2'},
    {'description': 'Todo 3'},
  ])

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)