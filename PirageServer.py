import CHIP_IO.GPIO as GPIO
import time
import requests
import logging
import socketserver
import threading
from http.server import BaseHTTPRequestHandler

logging.basicConfig(filename="/home/chip/Pirage/PirageServer.log", filemode='a', format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
logging.getLogger("urllib3").setLevel(logging.WARNING)

gpioGarageDoors = ["XIO-P0", "XIO-P1"]

#Enable relay to open or close garage door
def toggle_garage(index):
    try:
        if index < len(gpioGarageDoors):
            GPIO.output(gpioGarageDoors[index], GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(gpioGarageDoors[index], GPIO.HIGH)
            return 'Toggle sent to garage ' + str(index)
        else:
            return 'Garage door ' + str(index) + ' not configured'

    except Exception as e:
        logging.exception("Error toggling garage: " + e)


#Parses and responds to incoming http requests
class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
	    #Get index for commands that need it
            indexSplit = self.path.split('/')
            index = None
            if len(indexSplit) > 2 and indexSplit[2].isdigit():
                index = int(indexSplit[2])

            if '/ToggleGarage' in self.path and len(indexSplit) > 2:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(toggle_garage(index),'utf-8'))

        except Exception as e:
            logging.exception("Error processing http request: " + e)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
     pass

try:
    #Setup and start http server
    httpServer = ThreadedTCPServer(("", 80), GetHandler) 
    http_server_thread = threading.Thread(target=httpServer.serve_forever)
    http_server_thread.daemon = True
    http_server_thread.start()

    #Setup each GPIO pin that has a door attached
    for door in gpioGarageDoors:
        GPIO.setup(door, GPIO.OUT)
        GPIO.output(door, GPIO.HIGH)

    logging.info('Beginning Pirage loop')

    while True:
        print("Running...")
        time.sleep(60)
    
        #Handle all errors so loop does not end
        #except Exception as e:
        #    logging.exception("Error in loop: " + e) 

finally:
    #Close down http server and GPIO registrations
    httpServer.shutdown() 
    httpServer.server_close()
    GPIO.cleanup()
