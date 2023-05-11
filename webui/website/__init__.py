from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fdbcawejhfbwef'

    from .views import views,streaming

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(streaming, url_prefix='/')

    return app
