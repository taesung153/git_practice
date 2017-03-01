from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z][a-zA-Z]+$')
DATE_REGEX = re.compile(r'^\d\\\d\\\d$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9,_-]+.[a-zA-Z]+$')


# Create your models Managers here.
class UserManager(models.Manager):
	def register(self, postData):
		errors = []
		if len(postData['name']) < 3:
			errors.append('Name: must be at least 3 characters')
		if len(postData['username']) < 3:
			errors.append('Email mjust be validations!')
		if not NAME_REGEX.match(postData['name']):
			errors.append('Name: use letters only')
		if not EMAIL_REGEX.match(postData['username']):
			errors.append('Username: use letters only')
		check_user = self.filter(username=postData['username'])
		if check_user:
			errors.append('Username already registered, please login')
		if len(postData['password']) < 8:
			errors.append('Password: must be at least 8 characters')
		if not postData['password'] == postData['password_confirmation']:
			errors.append('Passwords do not match, please re-enter')

		if errors:
			return {'status':False, 'errors':errors}
		else:
			password = str(postData['password'])
			hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
			this_user = self.create(name=postData['name'], username=postData['username'], hire_date=postData['hire_date'], password=hashed_pw)
			print "NEW USER= ", this_user.id
			return {'status':True, 'user':this_user}

	def login(self, postData):
		errors = []
		try:
			this_user = self.get(username=postData['username'])
		except:
			errors.append('Email not registered, try again')
		else:
			password = str(postData['password'])
			hashed_pw = str(this_user.password)
			if bcrypt.hashpw(password, hashed_pw) != hashed_pw:
				errors.append('Password invalid, try again')

		if errors:
			return {'status':False, 'errors':errors}
		else:
			print "LOGGED IN= ", this_user.id
			return {'status':True, 'user':this_user}

class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	hire_date = models.DateField()
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
