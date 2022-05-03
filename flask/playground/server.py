from flask import Flask,render_template
app=Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', num = 3, color = "blue")

@app.route('/<string:color>/<int:num>')
def change(color, num):
    return render_template('index.html', color = color, num = num)

if __name__=="__main__":
    app.run(debug=True) 