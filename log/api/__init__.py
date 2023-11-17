# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    api.__init__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Flask
from threading import Thread

from .data.queue_consumer import QueueConsumer
# |--------------------------------------------------------------------------------------------------------------------|


def create_app() -> Flask:
    """
    Initialize Flask instance and register blueprints
    Returns:
        Flask: Flask app
    """
    app: Flask = Flask(__name__)
    
    # Start Queue Consumer in another thread
    Thread(target=QueueConsumer.run).start()
    
    from .routes.endpoints import bp
    app.register_blueprint(bp, url_prefix="/log")
    
    return app