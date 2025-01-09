from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Hobby (models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class CustomUser(AbstractUser):
    name = models.CharField(blank=True, max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    hobbies = models.ManyToManyField(Hobby, blank=True)

    def __str__(self):
        return self.username
    
    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "date_of_birth": self.date_of_birth,
            "hobbies": [hobby.as_dict() for hobby in self.hobbies.all()]
        }
        
class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"
