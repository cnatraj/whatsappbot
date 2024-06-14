import logging

from app import create_app

if __name__ == "__main__":
    app = create_app()
    logging.info("Flask app started")
    app.run()
else:
    gunicorn_app = create_app()
