# Dropzone Action Info
# Name:                 macOS Auto Image Tagger
# Description:          Automatically adds tags based on the result of image recognition.
# Handles:              Files
# Creator:              Kolja Nolte, Supawadee Sakunkloy
# URL:                  https://www.kolja-nolte.com
# Events:               Dragged
# KeyModifiers:         Command, Option, Control, Shift
# SkipConfig:           No
# RunsSandboxed:        Yes
# Version:              1.0.0
# MinDropzoneVersion:   3.5

import os
import requests
import mac_tag


def dragged():
	api_key = 'acc_ae3476459bae83f'
	api_secret = '69c35cd52aab20144225351c36e00765'
	api_url = 'https://api.imagga.com'
	api_tag_url = api_url + '/v2/tags?image_upload_id=%s&threshold=30'
	image_path = items

	for item in items:
		if not os.path.exists(item):
			print("Image could not be found.")

			exit(404)

		response = requests.post(
			'https://api.imagga.com/v2/uploads',
			auth=(api_key, api_secret),
			files={'image': open(item, 'rb')})

		if not response.status_code == 200 or not response.json()['status']['type'] == 'success':
			exit()

		image_id = response.json()['result']['upload_id']

		response = requests.get(
			api_tag_url % image_id,
			auth=(api_key, api_secret)
		)

		if not response.status_code == 200 or not response.json()['status']['type'] == 'success':
			exit()

		tags = response.json()['result']['tags'][:10]

		for tag in tags:
			the_tag = tag['tag']
			mac_tag.add(the_tag['en'], item)
