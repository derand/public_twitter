#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Andrey Derevyagin'
__email__ = '2derand@gmail.com'
__copyright__ = 'Copyright © 2012, Andrey Derevyagin'


import webapp2
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.ext import db
import logging

import requests
from oauth_hook import OAuthHook
from constants import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET, API_URL
from tw_db import Task
import time

def do_task(task):
	client = memcache.get('client')
	if client is None:
		OAuthHook.consumer_key = CONSUMER_KEY
		OAuthHook.consumer_secret = CONSUMER_SECRET
		oauth_hook = OAuthHook(TOKEN, TOKEN_SECRET, header_auth=True)
		client = requests.session(hooks={'pre_request': oauth_hook})
		if not memcache.add('client', client, 60*60*24):
			logging.error('Memcache set failed for key "client".')
	response = None
	if task.action == 'tweet':
		response = client.post(API_URL + 'statuses/update.json', {
			'status': task.param,
			#'wrap_links': True,
		})
	elif task.action == 'delete':
		response = client.post(API_URL + 'statuses/destroy/%s.json'%task.param, {
		})
	elif task.action == 'retweet':
		response = client.post(API_URL + 'statuses/retweet/%s.json'%task.param, {
			#'id': task.param,
		})
	elif task.action == 'follow':
		response = client.post(API_URL + 'friendships/create.json', {
			'screen_name': task.param,
		})
	elif task.action == 'unfollow':
		response = client.post(API_URL + 'friendships/destroy.json', {
			'screen_name': task.param,
		})
	elif task.action == 'direct_message':
		response = client.post(API_URL + 'direct_messages/new.json', {
			'screen_name': task.param,
			'text': task.ex_param
		})
	elif task.action == 'verify':
		response = client.post(API_URL + 'account/verify_credentials.json', {
		})
	elif task.action == 'update_name':
		response = client.post(API_URL + 'account/update_profile.json', {
			'name': task.param,
		})
	elif task.action == 'update_url':
		response = client.post(API_URL + 'account/update_profile.json', {
			'url': task.param,
		})
	elif task.action == 'update_location':
		response = client.post(API_URL + 'account/update_profile.json', {
			'location': task.param,
		})
	elif task.action == 'favorite':
		response = client.post(API_URL + 'favorites/create.json', {
			'id': task.param,
		})
	elif task.action == 'un-favorite':
		response = client.post(API_URL + 'favorites/destroy.json', {
			'id': task.param,
		})
	elif task.action == 'report_spam':
		response = client.post(API_URL + 'users/report_spam.json', {
			'screen_name': task.param,
		})
	else:
		task.status = 'error'

	if not memcache.set('last_time', time.time(), 60*60*24):
		logging.error('Memcache set failed for key "last_time".')
	return response



class Worker(webapp2.RequestHandler):
	def get(self):
		if not self.request.headers.has_key('X-AppEngine-Cron'):
			self.error(404)
			#self.response.out.write('404 error html page')
			return 
		query = db.GqlQuery("SELECT * FROM Task WHERE status = :1 ORDER BY timestamp", 'ready')
		for task in query.run(limit=1):
			task.status = 'completed'

			response = do_task(task)

			task.put()
			if response is not None:
				self.response.out.write(response.text)


class PutMessage(webapp2.RequestHandler):
	def get(self):
		task = Task(action='tweet',
					param='%d'%time.time(),
					status='ready')
		task.put()


app = webapp2.WSGIApplication([
							   ('/cron/worker', Worker),
							   ('/cron/test_put', PutMessage),
							  ], debug=True)
