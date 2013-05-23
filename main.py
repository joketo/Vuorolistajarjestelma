from bottle import route, run, template
import random

def rand():
    return random.choice([True,False])

@route("/")
def etusivu():
    return template("front")

@route("/login")
def login_page():
    return template("login")

@route("/test")
def test():
    return template("test", nimet=["a", "b", "c"], rand=rand)

@route("/possibleCustomers")
def asiakkaat():
    return template("possibleCustomers", hoitajat =["a", "b"], potilaat =["i", "j", "k", "h"], rand=rand)

if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)

