from app import app, db


def create():
    if __name__ == "__main__":
        db.create_all()
        app.run(
            debug=True
        )
