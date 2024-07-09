from Flask import Flask
app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Hello World!'

if __name__ == '__main__' : app.run(debug=True)