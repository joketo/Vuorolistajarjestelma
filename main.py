from bottle import route, run, template

@route('/')
def etusivu():
    return """
    <h1>Tähän tulee etusivu!</h1>
    <a href="/login">Kirjaudu</a>
    """

@route("/login")
def login():
    return template("login")



if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)
    
