from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from typing import List, Dict

class Hobby(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def as_dict(self) -> Dict:
        return {"id": self.id, "name": self.name}
class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, through='UserHobby', related_name='users')

    def __str__(self):
        return self.username
    def as_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "date_of_birth": str(self.date_of_birth),
            "hobbies": [hobby.as_dict() for hobby in self.hobbies.all()],
        }

class UserHobby(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} enjoys {self.hobby.name}"

class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        CustomUser, related_name='sent_friend_requests', on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        CustomUser, related_name='received_friend_requests', on_delete=models.CASCADE
    )
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        status = "Accepted" if self.is_accepted else "Pending"
        return f"{self.from_user.username} -> {self.to_user.username} ({status})"

    def as_dict(self):
        return {
            "id": self.id,
            "from_user": {"id": self.from_user.id, "name": self.from_user.username},
            "to_user": {"id": self.to_user.id, "name": self.to_user.username},
            "is_accepted": self.is_accepted,
            "created_at": self.created_at.isoformat(),
        }