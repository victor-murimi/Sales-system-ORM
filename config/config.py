import os
class Development():
    SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    SECRET_KEY=os.getenv("SECRET_KEY")
    DEBUG=os.getenv("DEBUG")
    FLASK_APP=os.getenv("FLASK_APP")
    FLAKS_ENV=os.getenv("FLASK_ENV")

    