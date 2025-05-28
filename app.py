from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html') # Hier wird das Template gerendert

if __name__ == '__main__':
    app.run(debug=True)