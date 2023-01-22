from app import config
from app import routes
from app.http import app

if __name__ == "__main__":
    config.init()

    routes.register_routes(app)

    from app.database import init

    init()

    app.run(debug=config.CONFIG.DEV, host=config.CONFIG.HOST)
