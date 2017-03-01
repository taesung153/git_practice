from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from ..LoginReg.models import User


class ItemManager(models.Manager):
	def show_items(self, postData):
		user = User.objects.get(id=postData['user_id'])
		items = self.filter(users=user)
		return {'status':True, 'items':items}

	def create_item(self, postData):
		if len(postData['item_name']) < 3:
			errors.append('Name: must be at least 3 characters')
			errors = []
			return {'status':False, 'errors':errors}
		user = User.objects.get(id=postData['user_id'])
		item = self.create(name=postData['item_name'], creator=user)
		return {'status':True, 'item':item}

	def delete_item(self, postData):
		try:
			item = self.get(id=postData['item_id'])
		except ObjectDoesNotExist:
			return {'status':False}
		user = User.objects.get(id=postData['user_id'])
		if item.creator != user:
			return {'status':False}
		users = User.objects.all()
		for user in users:
			item.users.remove(user)
		item.delete()
		return {'status':True}

	def add_item_to_list(self, postData):
		try:
			item = self.get(id=postData['item_id'])
		except ObjectDoesNotExist:
			return {'status':False}
		try:
			user = User.objects.get(id=postData['user_id'])
		except ObjectDoesNotExist:
			return {'status':False}
		item.users.add(user);
		return {'status':True, 'item':item}


	def remove_item_from_list(self, postData):
		try:
			item = self.get(id=postData['item_id'])
		except ObjectDoesNotExist:
			return {'status':False}
		try:
			user = User.objects.get(id=postData['user_id'])
		except ObjectDoesNotExist:
			return {'status':False}
		item.users.remove(user)
		return {'status':True}

class Item(models.Model):
	name = models.CharField(max_length=255)
	users = models.ManyToManyField(User, related_name="item_user")
	creator = models.ForeignKey(User, related_name="item_creator")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ItemManager()

class Appt(models.Model):
	task = models.CharField(max_length=255)
	date = models.DateField()
	time = models.TimeField()
	status = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
