import os
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class InstantComment(db.Model):
	name = db.StringProperty(required=True)
	audio = db.BlobProperty(default=None)
	owner = db.UserProperty(auto_current_user=True)
	created_at = db.DateTimeProperty(auto_now=True)

	@staticmethod
	def comments_for_user(user):
		return db.GqlQuery("SELECT * FROM InstantComment WHERE owner = :1", user).fetch(10)
		
class CommentHandler(webapp.RequestHandler):
	def get(self):
		comment = InstantComment.get(db.Key(self.request.get('cid')))
		if comment and comment.audio:
			self.response.headers['Content-Type'] = 'audio/mp3'
			self.response.out.write(comment.audio)

	def post(self):
		new_comment = InstantComment(name = self.request.get('name'),
									 audio = self.request.get('audiofile'),
									 owner = users.get_current_user())
		new_comment.put()
		self.redirect('/')

class MainPage(webapp.RequestHandler):
    def get(self):
		user = users.get_current_user()
		logout_url = users.create_logout_url(self.request.uri)
		
		my_comments = InstantComment.comments_for_user(user)
		comments_names = []
		for comment in my_comments:
			logging.info("Coment: [%s]", comment.name)
			comments_names.append(comment.name)
			
		template_values = {
			'nickname': user.nickname(),
			'logout_url': logout_url,
			'comments': my_comments
		}
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication(
                                     [('/', MainPage), 
                                      ('/upload', CommentHandler),
                                      ('/get', CommentHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()