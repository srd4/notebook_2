from django.db import models
from django.conf import settings

from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Container(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=200)
    parentContainer = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, default=1)
    lastOpened = models.DateTimeField(auto_now=True)
    timesOpened = models.IntegerField(default=1)
    collapsed = models.BooleanField(default=True)
    seeingActionables = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        #Children containers fall into parent container after their container is deleted.
        for i in self.getChildren():
            i.parentContainer = self.parentContainer
            i.name = self.name + " : " + i.name
            i.save()

        #Items in container fall into parent container after their container is deleted.
        for i in self.getItems():
            if self.parentContainer != None:
                i.parentContainer = self.parentContainer
            else:
            #or on inbox if parentContainer = None.
                i.parentContainer = Container.objects.get(pk=1, owner=self.owner)
            i.save()
        return super().delete(*args, **kwargs)

    def get_parentContainer(self):
        return self.parentContainer

    def __str__(self):
        return self.name

    def add_timesOpened(self):
        """increases by one timesOpened field on model object, saves the model object."""
        self.timesOpened += 1
        self.save()

    def add_lastOpened(self):
        """updates lastOpened field on model object, saves the model object."""
        self.lastOpened = models.DateTimeField(auto_now=True)
        self.save()

    def getChildren(self):
        return Container.objects.filter(parentContainer=self.pk, owner=self.owner).order_by('-timesOpened')
    
    def getItems(self):
        return Item.objects.filter(parentContainer=self.pk, owner=self.owner)

    def toggleCollapsed(self):
        if self.collapsed == True:
            self.collapsed = False
        else:
            self.collapsed = True
        self.save()
    
    def toggleTab(self):
        if self.seeingActionables == True:
            self.seeingActionables = False
        else:
            self.seeingActionables = True
        self.save()

    def countTreeItems(self):
        i = len(self.getItems())
        for child in self.getChildren():
            i += child.countTreeItems()
        return i



class Item(models.Model):
    actionable = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    statement = models.TextField(max_length=140)
    parentContainer = models.ForeignKey(Container, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    parentItem = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(null=True, default=None)

    def save(self, *args, **kwargs):
        self.createItemStatementVersion()
        return super().save(*args, kwargs)

    def createItemStatementVersion(self):
        old_exists = Item.objects.filter(pk=self.pk, owner=self.owner).exists()
        if old_exists:
            old = Item.objects.get(pk=self.pk)
            ItemStatementVersion.objects.get_or_create(statement=old.statement, defaults={'parentItem' :self, 'created_at': old.updated_at, 'owner':self.owner})

    def __str__(self):
        return self.statement

    def get_parentContainer(self):
        return Container.objects.get(pk=self.parentContainer.pk, owner=self.owner)
    
    def get_parentItem(self):
        return Item.objects.get(pk=self.parentItem)

    def get_versions(self):
        return ItemStatementVersion.objects.filter(parentItem_id=self.pk, owner=self.owner)
    
    def toggleDone(self):
        if self.done:
            self.done = False
            self.save()
            self.completed_at = self.updated_at
        else:
            self.done = True
            self.save()
            self.completed_at = self.updated_at
        self.save()


class ItemStatementVersion(models.Model):
    statement = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    parentItem = models.ForeignKey(Item, null=False, on_delete=models.CASCADE)
    whatever = models.TextField(max_length=140)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.statement


