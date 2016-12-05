#!/usr/bin/python

import webbrowser


class Movie():
	# Init
	def __init__(self, title, storyline, poster_image, trailer_youtube):
		self.title = title
		self.storyline = storyline
		self.poster_image_url = poster_image
		self.trailer_youtube_url = trailer_youtube

	# Show movie trailer on Youtube
	def show_trailer(self):
		webbrowser.open(self.trailer_youtube_url)
		