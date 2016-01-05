from flask import Flask, render_template, make_response, request
from flask.ext.bootstrap import Bootstrap
from mprequest import WhiteList


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET'])
def index():
    response = make_response('<h1>this document carries a cookie')
    response.set_cookie('answer','42')
    return response


@app.route('/user/<username>')
def user1(username):
    return render_template('test2.html', username=username)


@app.errorhandler(400)
def page_not_found(e):
    return '<h1>not found</h1>', 400


@app.route('/', methods=['POST'])
def mobile():
    mobiles = request.get_json()['mp']
    wl = WhiteList()
    wl.setusername('')
    wl.setpassword('')
    wl.addmobile(mobiles)
    res = wl.savemobile()
    wl.close()
    return str(res)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
