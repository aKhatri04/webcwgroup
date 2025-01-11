from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class Hobby(models.Model):
    """
    Represents a hobby.

    Attributes:
        name (str): The name of the hobby.
    """
    
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    def as_dict(self):
        return {"id":self.id, 
                "name":self.name, 
                "api": reverse('hobby-api', args=[self.id]),
                }

class CustomUser(AbstractUser):
    
    """
    Represents a custom user with additional profile fields.

    Attributes:
        name (str): Full name.
        email (str): Unique email.
        date_of_birth (date): User's date of birth.
        hobbies (ManyToManyField): User's list of hobbies.
    """
    
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, through='UserHobby', related_name="users")

    def __str__(self):
        return self.username

    def as_dict(self):
        
        return {"id":self.id, 
                "name":self.name, 
                "email":self.email, 
                "date_of_birth":self.date_of_birth, 
                "hobbies":[[hobby.id, hobby.name] for hobby in self.hobbies.all()],
                "api": reverse('user-api', args=[self.id]),
                }
    
    def current_as_dict(self):
        return {"id":self.id, 
                "name":self.user, 
                "email":self.hobby, 
                "date_of_birth":self.date_added, 
                "hobbies":[[hobby.id, hobby.name] for hobby in self.hobbies.all()],
                "password":self.password,
                }
        
class UserHobby(models.Model):
    
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} enjoys {self.hobby.name}"

    
    def as_dict(self):
        return {
            "id":self.id, 
                "user": self.user.as_dict(),
                "hobby":self.hobby.as_dict(),
                "api": reverse('user-hobby-api', args=[self.id]),
        }


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"