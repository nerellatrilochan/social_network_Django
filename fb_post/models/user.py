from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    profile_pic = models.TextField()

    def __str__(self):
        return f"<User: {self.name}>"