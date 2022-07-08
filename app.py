from flask import Flask, render_template, request, redirect, session
from rockpaperscissors import play_rps
from dbcommands import create_user, write_game, update_user


app = Flask(__name__)
app.secret_key = "unaclaveimposibledeadivinar"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        if request.values.get("username") == "":
            return redirect("/")
        else:
            session["username"] = request.values.get("username")
            session["credits"] = 0
            session["games_played"] = 0
            session["games_won"] = 0
            session["message"] = "Start playing! Choose your bet below:"
            session["user_id"] = create_user(**session)
            print(session["user_id"])
            return redirect("/play")


@app.route("/play", methods=["GET", "POST"])
def play():
    if request.method == "GET":
        if session.get("username", None) is None:
            return redirect("/")
        else:
            return render_template("game.html", **session,
                                   game_disabled=True if session["credits"] < 3 else False,
                                   add_disabled=True if session["credits"] > 0 else False)
    if request.method == "POST":
        session["games_played"] += 1
        choice = list(request.form)[0]
        result, message = play_rps(choice)
        write_game(session["user_id"], result == "win", session["credits"])
        session["credits"] -= 3
        session["message"] = message
        if result == "win":
            session["credits"] += 4
            session["games_won"] += 1
        return redirect("/play")


@app.route("/add", methods=["POST"])
def add_creds():
    if session["credits"] == 0:
        session["credits"] = 10
        return redirect("/play")


@app.route("/stats", methods=["GET"])
def stats():
    return redirect("/")


@app.route("/submit", methods=["GET"])
def submit():
    update_user(**session)
    return redirect("/stats")


if __name__ == "__main__":
    app.run(debug=True)
