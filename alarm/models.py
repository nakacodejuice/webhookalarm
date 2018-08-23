from django.db import models
import datetime

class Request(models.Model):
    requesttext = models.TextField()
    DateTimeField = models.DateTimeField('date created', auto_now_add=True)
    Messanger = models.CharField(max_length=20,default='viber')

class Alarms(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    text = models.TextField()
    DateTimeField = models.DateTimeField('date created', auto_now_add=True)
    sent = models.BooleanField()
    DateTimesent = models.DateTimeField()
    def __str__(self):
        return self.DateTimeField + '-' + self.text

class users(models.Model):
    chatid = models.CharField(max_length=24, primary_key=True)
    group = models.CharField(max_length=20,default='')
    name = models.TextField()
    tel = models.CharField(max_length=20)
    def __str__(self):
        return self.name + '-' + self.tel