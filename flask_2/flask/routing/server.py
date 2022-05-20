from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return 'hello world!'

@app.route('/<name>')
def dojo(name):
    return name

@app.route('/say/<name>')
def name(name):
    return "Hi " + name

@app.route('/repeat/<int:num>/<string:name>')
def mult_say(num, name):
    output = ''

    for i in range(0, num):
        output+= f'<p>{name}</p>'
    return output
    
    return num * name



if __name__ == "__main__":
    app.run(debug=True)