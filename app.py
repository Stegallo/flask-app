from flask import Flask, redirect, request, session, url_for, render_template
import requests
import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your_secret_key")  # Replace in production
#
STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REDIRECT_URI = "https://stefanogallottiusa.pythonanywhere.com/authorized"
STRAVA_REDIRECT_URI = "http://127.0.0.1:5000/authorized"
AUTHORIZATION_BASE_URL = "https://www.strava.com/oauth/authorize"
TOKEN_URL = "https://www.strava.com/oauth/token"
SCOPE = ["activity:read_all"]

@app.route("/")
def index():
    return '<a href="/authorize">Connect with Strava</a>'

@app.route("/authorize")
def authorize():
    auth_url = (
        f"https://www.strava.com/oauth/authorize?client_id={STRAVA_CLIENT_ID}"
        f"&redirect_uri={STRAVA_REDIRECT_URI}"
        f"&response_type=code&scope=read,activity:read"
    )
    return redirect(auth_url)

@app.route("/authorized")
def authorized():
    code = request.args.get("code")
    token_response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
        },
    )
    token_data = token_response.json()
    session["access_token"] = token_data["access_token"]
    return redirect(url_for("activities"))

@app.route("/activities")
def activities():
    access_token = session.get("access_token")

    if not access_token:
        return redirect(url_for("index"))

    response = requests.get(
        "https://www.strava.com/api/v3/athlete/activities",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"per_page": 5, "page": 1}
    )
    if response.status_code != 200:
        return f"Error fetching activities: {response.text}"

    data = response.json()
    return render_template("activities.html", activities=data)

if __name__ == "__main__":
    app.run()
