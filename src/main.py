from app import app
from routes import register_routes


if __name__ == "__main__":
    register_routes(app)
    app.run(debug=True, host="0.0.0.0")
