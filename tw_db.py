#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Andrey Derevyagin'
__email__ = '2derand@gmail.com'
__copyright__ = 'Copyright © 2012, Andrey Derevyagin'


import datetime
from google.appengine.ext import db

all_actions = [
				'tweet', 'delete', 'follow', 'unfollow', 'retweet', 'direct_message',
				'update_name', 'update_url', 'update_location', 'favorite', 'un-favorite',
				'report_spam'
			  ]

class Task(db.Model):
	timestamp = db.DateTimeProperty(auto_now=True)
	#action = db.IntegerProperty(required=True)
	action = db.StringProperty(required=True, choices=set(all_actions))
	param  = db.StringProperty(required=True)
	ex_param = db.StringProperty()
	status = db.StringProperty(required=True, choices=set(['completed', 'ready', 'waiting', 'error']))



