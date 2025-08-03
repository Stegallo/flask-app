from flask import Flask, render_template
import os
import requests

app = Flask(__name__)

@app.route("/")
def index():
    """Display the last 5 Strava activities using the Strava API."""
    access_token = os.getenv("STRAVA_ACCESS_TOKEN")
    activities = []
    if access_token:
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"per_page": 5, "page": 1}
        try:
            response = requests.get(
                "https://www.strava.com/api/v3/athlete/activities",
                headers=headers,
                params=params,
                timeout=10,
            )
            if response.status_code == 200:
                activities = response.json()
        except requests.RequestException:
            # If there's an error making the request, keep activities empty
            activities = []
    return render_template("index.html", activities=activities)

if __name__ == "__main__":
    # Enable debug mode when running locally
    app.run(debug=True)
