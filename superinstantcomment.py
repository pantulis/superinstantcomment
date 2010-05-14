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
	is_global = db.BooleanProperty(default=False)
	
	@staticmethod
	def comments_for_user(user):
		return db.GqlQuery("SELECT * FROM InstantComment WHERE owner = :1", user).fetch(10)
		
	@staticmethod
	def global_comments():
		return db.GqlQuery("SELECT * FROM InstantComment WHERE is_global =:1", True).fetch(100)
		
class CommentHandler(webapp.RequestHandler):
	def get(self):
		comment = InstantComment.get(db.Key(self.request.get('cid')))
		if comment and comment.audio:
			self.response.headers['Content-Type'] = 'audio/mp3'
			self.response.out.write(comment.audio)

	def post(self):
		new_comment = InstantComment(name = self.request.get('name'),
									 audio = self.request.get('audiofile'),
									 owner = users.get_current_user(),
									 is_global = True if self.request.get('is_global') else False)
		new_comment.put()
		self.redirect('/')

class MainPage(webapp.RequestHandler):
    def get(self):
		user = users.get_current_user()
		logout_url = users.create_logout_url(self.request.uri)
		
		my_comments = InstantComment.comments_for_user(user)
		global_comments = InstantComment.global_comments()

		comments_names = []
		for comment in my_comments:
			logging.info("Coment: [%s]", comment.name)
			comments_names.append(comment.name)
			
		template_values = {
			'nickname': user.nickname(),
			'logout_url': logout_url,
			'is_admin': users.is_current_user_admin(),
			'global_comments': global_comments,
			'my_comments': my_comments
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