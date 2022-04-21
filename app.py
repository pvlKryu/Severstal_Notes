from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return ("Severstal Notes")


if __name__ == "__main__":
    app.run(debug=True)
