#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import webapp2
from google.appengine.ext import db

from tw_db import Task, all_actions

import json
from google.appengine.api import memcache
import requests
from oauth_hook import OAuthHook
from constants import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET, API_URL


class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.redirect("/index.html")
		return
		path = os.path.join(os.path.dirname(__file__), "index.html")
		self.response.out.write(template.render(path, template_values))


class NewAction(webapp2.RequestHandler):
	def post(self):
		action = self.request.get('action')
		if action in all_actions:
			param = self.request.get('param')
			ex_param = self.request.get('ex_param')
			task = Task(action=action, param=param, status='waiting')
			if ex_param is not None:
				task.ex_param = ex_param
			if action in ['tweet', 'delete', 'follow', 'unfollow', 'retweet', 'direct_message',
						  'update_name', 'update_url', 'update_location', 'favorite', 'un-favorite']:
				task.status = 'ready'
			task.put()

		if task.status == 'ready':
			client = record = memcache.get('client')

		if self.request.get('redirect_url'):
			self.redirect(self.request.get('redirect_url'))
		else:
			self.response.out.write('{"status": "ok"}')


app = webapp2.WSGIApplication([
								('/', MainHandler),
								('/new_action', NewAction)
							  ], debug=True)
