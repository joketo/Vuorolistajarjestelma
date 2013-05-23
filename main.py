from bottle import route, run, template

@route('/')
def etusivu():
    return template("front")

@route("/login")
def login():
    return template("login")



if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)
    
