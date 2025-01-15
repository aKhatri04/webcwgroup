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
                "api": reverse('hobby_api', args=[self.id]),
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
                "date_of_birth": str(self.date_of_birth), 
                "hobbies":[{"id": hobby.id, "name": hobby.name} for hobby in self.hobbies.all()],
                "api": reverse('user_api', args=[self.id]),
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
                "api": reverse('user_hobby_api', args=[self.id]),
        }


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"


class FriendRequest(models.Model):
    """
    Represents a friend request.

    Attributes:
        from_user (CustomUser): The user who sent the request.
        to_user (CustomUser): The user receiving the request.
        is_accepted (bool): Whether the request has been accepted.
        created_at (datetime): When the request was created.
    """
    from_user = models.ForeignKey(CustomUser, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='received_friend_requests', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({'Accepted' if self.is_accepted else 'Pending'})"

    def as_dict(self):
        return {
            "id": self.id,
            "from_user": self.from_user.as_dict(),
            "to_user": self.to_user.as_dict(),
            "is_accepted": self.is_accepted,
            "created_at": self.created_at.isoformat(),
        }