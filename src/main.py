from app.config import CONFIG
from app import routes
from app.http import app

if __name__ == "__main__":
    routes.register_routes(app)

    app.run(debug=CONFIG.DEV, host=CONFIG.HOST)
