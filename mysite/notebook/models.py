from django.db import models
from django.conf import settings

# there are boxes. like the inbox, where everything is added without filter. the actionable, where items that represent actions to-do are stored.
# and non-actionable, where the opposite kind of items are stored (ideas). then all projects are also boxes.
# inside actionables then, you can find more boxes that represent projects ahd have items.
# so boxes can have sub-boxes and shit.
# and boxes store items and other boxes.
# an item inside a box that has other boxes, is an item that has not been sorted into these box's sub-boxes.

class Box(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Idea(models.Model):
    done = models.BooleanField(default=False)
    text = models.TextField(max_length=280)
    actionable = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    box = models.ForeignKey(Box, null=True, on_delete=models.SET_DEFAULT, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

        