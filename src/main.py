from transactions.http import routes, app

if __name__ == "__main__":
    routes.register_routes(app.app)

    app.app.run(debug=True, host="0.0.0.0")
