from transactions.config import CONFIG
from transactions import routes
from transactions.http import app

if __name__ == "__main__":
    routes.register_routes(app)

    app.run(debug=CONFIG.DEV, host=CONFIG.HOST)
