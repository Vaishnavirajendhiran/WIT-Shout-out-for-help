#!/usr/bin/env python3
import json
import time
import shutil
import os
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from config import path_to_recordings_, path_to_archive_, path_to_output_

path_to_recordings = path_to_recordings_
path_to_archive = path_to_archive_
authenticator = IAMAuthenticator('BZasOHJgtee32ZrY5edWYUGAiIAL8LgIio1rICJryf4G')
count = 1
speech_to_text = SpeechToTextV1(authenticator=authenticator)

speech_to_text.set_service_url('https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/761a9b6a-3b66-40b5-8b71-35963b364c76/v1/recognize')

class MyRecognizeCallback(RecognizeCallback):
	def __init__(self):
		RecognizeCallback.__init__(self)
	def on_hypothesis(self, hypothesis):
		the_text = {"text":hypothesis}
		#output_save = "/home/nandni_yadav/speech-to-text/output/"+count+".json"
		output_save = path_to_output_+hypothesis.replace(" ","_")+".json"
		with open(output_save,'w') as outfile:
			json.dump(the_text,outfile)
		print(the_text)
		#print(json.dumps(hypothesis,indent=2))
	#def on_transcription(self, transcript):
		#print(transcript)
		#print(json.dumps(transcript, indent=2))
	#def on_data(self, data):
	#	print(json.dumps(data, indent=2))
	def on_error(self, error):
		print('Error received: {}'.format(error))
	def on_inactivity_timeout(self, error):
		print('Inactivity timeout: {}'.format(error))


myRecognizeCallback = MyRecognizeCallback()
before = dict([(f, None) for f in os.listdir(path_to_recordings)])
while 1:
	print("waiting...")
	after = dict([(f,None) for f in os.listdir(path_to_recordings)])
	added = [f for f in after if not f in before]
	if added:
		for root, dirs, files in os.walk(path_to_recordings):
			for filename in files:
				count = count + 1
				audio_file1 = path_to_recordings+"/"+filename
				if os.path.exists(audio_file1):
					with open(join(dirname(__file__), './.', audio_file1),'rb') as audio_file:
						audio_source = AudioSource(audio_file)
						speech_to_text.recognize_using_websocket(
						audio=audio_source,content_type='application/octet-stream',
						recognize_callback=myRecognizeCallback,
						model='en-US_BroadbandModel',
						max_alternatives=3
						)
				shutil.move(audio_file1, path_to_archive)
	time.sleep(3)
	before=after
