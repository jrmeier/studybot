from flask import Flask, send_from_directory
from flask import request
import json
import engine
#import api.engine
app = Flask(__name__)


@app.route("/")
def hello():
	return send_from_directory('./','./index.html')
@app.route('/botstyle.css')
def static_proxy():
	return send_from_directory('./','./botstyle.css')

@app.route("/quizlet/", methods = ['GET','POST'])
def quizlet():
	print "quizlet endpoint"
	return "hey you found the quizlet endpoint!"

@app.route("/api/", methods=['GET','POST'])
def api():
	if request.method == 'POST':
		data = json.loads(request.data)
		print data
		smoochid = data[u'appUser'][u'_id']
        	device = data[u'appUser'][u'devices'][0][u'platform']
        	postback = None
        	user_text = None
        	metadata = None
		
		try:
            		givenName = data['appUser']['clients'][0]['displayName']
        	except:
            		givenName = "Name Unavailable"

        # Either a postback or the user's text will be available in the json request
        	try:
            		postback = data['postbacks'][0]['action']['payload']
            		try:
                		metadata = data['postbacks'][0]['action']['metadata']
            		except:
                		pass
        	except:
            		user_text = data[u'messages'][0][u'text']

        	print "Smooch ID: ", smoochid
        	print "User Text: ", user_text
       	 	print "Postback: ", postback
        	print "Device: ", device
        	print "Metadata: ", metadata
        	print "givenName", givenName
       	 	print "smoochAppName", app
        	try:
			print "hey this will be the compute function!"
			
			return "error"
            		#engine.compute(smoochid=smoochid, msg=user_text, device=device, postback=postback, metadata=metadata, givenName=givenName, smoochAppName=smoochAppName)
		except:
			print "something didn't work"
			return "error :("
	else:
		print "this was a get request bruh"
		return "why"
	print "Done!"
if __name__ == "__main__":
    app.run(host='0.0.0.0',port='80')
