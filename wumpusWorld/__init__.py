#*******************************Imports********************************
from flask import Flask

#*******************************Script commands********************************
app = Flask(__name__)

#Importing the routes
from wumpusWorld import routes