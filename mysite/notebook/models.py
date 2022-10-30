from django.db import models

# there are boxes. like the inbox, where everything is added without filter. the actionable, where items that represent actions to-do are stored.
# and non-actionable, where the opposite kind of items are stored (ideas). then all projects are also boxes.
# inside actionables then, you can find more boxes that represent projects ahd have items.
# so boxes can have sub-boxes and shit.
# and boxes store items and other boxes.
# an item inside a box that has other boxes, is an item that has not been sorted into these box's sub-boxes.

class Box(models.Model):
    box_name = models.CharField(max_length=128)

    def __str__(self):
        return self.box_name


class Idea(models.Model):
    box = models.ForeignKey(Box, null=True, on_delete=models.SET_DEFAULT, default=1) #default is 1, or the inbox.
    idea_text = models.TextField(max_length=280)
    actionable = 0

    def __str__(self):
        return self.idea_text
