from flask import Flask
from app.routes import main

def create_app():
    app = Flask(__name__)

    # File upload config
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

    app.register_blueprint(main)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)