from app import create_app, db

app = create_app()

# O PythonAnywhere importa esta variável como "application" no arquivo WSGI.
application = app

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
