from flask import Flask

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """Return a simple greeting for the home page."""
    return "Hello from your Flask app! - Version 0.1.0"


if __name__ == "__main__":  # pragma: no cover
    # When running locally, enable debug mode for autoreload and easier debugging.
    app.run(debug=True)
