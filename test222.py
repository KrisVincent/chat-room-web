
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from sqlalchemy.orm import session

# https://flask-socketio.readthedocs.io/en/latest/
# https://github.com/socketio/socket.io-client

app = Flask(__name__)

app.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc'
socketio = SocketIO( app )

@app.route( '/' )
def hello():
  return render_template( 'test.html' )

def messageRecived():
  print( 'message was received!!!' )

@socketio.on( 'check' )
def handle_my_custom_event( ):
	print(session["username"])



@socketio.on( 'check1' )
def handle_my_custom_event1( json):
	session["username"] = json["username"]
  
 

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  
  print( 'recived my event: ' + str( json ) )
  socketio.emit( 'my response', json, callback=messageRecived )
  print(type(json)) 


if __name__ == '__main__':
  socketio.run( app, debug = True )