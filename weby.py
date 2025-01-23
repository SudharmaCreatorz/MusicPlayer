from flask import Flask

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Sudharma Music Player is running!", 200

if __name__ == "__main__":
    # Use the port Heroku provides via the environment variable `PORT`
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
