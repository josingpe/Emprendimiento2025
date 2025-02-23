from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenido al Sistema de Nómina en la Web"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
