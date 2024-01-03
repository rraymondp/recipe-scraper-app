from flask import Flask
from views import views   #import views variable from views.py
from waitress import serve

# Main Screen for the website

app = Flask(__name__) #creating/intialize the flask application
app.register_blueprint(views, url_prefix="/") # access any route if the url prefix is "/"


if __name__ == "__main__": #running the application
    serve(app, host="0.0.0.0", port=8000)