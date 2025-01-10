from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


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
        
class UserHobby(models.Model):
    """
    A model representing the relationship between a user and a hobby.

    Attributes:
        user (ForeignKey): The user who has the hobby.
        hobby (ForeignKey): The hobby assigned to the user.
    Methods:
        __str__(): Returns a string representation of the user's hobby.
        as_dict(): Returns a dictionary representation of the user-hobby relationship.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.username} enjoys {self.hobby.name}"

    def as_dict(self):
        return {
            "id": self.id,
            "user": {
                "id": self.user.id,
                "username": self.user.username,
                "name": self.user.name,
                "email": self.user.email,
            },
            "hobby": self.hobby.as_dict(),
            "api": reverse('user-hobby-api', args=[self.id]),
        }

class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"
