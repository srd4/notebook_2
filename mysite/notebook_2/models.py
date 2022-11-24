from django.db import models
from django.conf import settings

from django.utils import timezone


class Container(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=140)
    parentContainer = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lastOpened = models.DateTimeField(default=timezone.now)
    timesOpened = models.IntegerField(default=1)
    collapsed = models.BooleanField(default=True)
    seeingActionables = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        #Children containers fall into parent container after their container is deleted.
        for i in self.getChildren():
            i.parentContainer = self.parentContainer
            #children's name is changed to show the relationship that existed.
            i.name = self.name + " : " + i.name
            i.save()

        #Items in container fall into parent container after their container is deleted.
        for i in self.getItems():
            if self.parentContainer != None:
                i.parentContainer = self.parentContainer
            elif Container.objects.filter(owner=self.owner).exists():
            #or on first user's container if parentContainer = None -Null if such container doesn't exist as it is the Item model's default.
                i.parentContainer = Container.objects.filter(owner=self.owner).first()
            i.save()
        return super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    def add_timesOpened(self):
        self.timesOpened += 1
        self.save()

    def add_lastOpened(self):
        self.lastOpened = timezone.now()
        self.save()

    def getChildren(self):
        """sorted by used on templates containersView's template"""
        return Container.objects.filter(parentContainer=self.pk, owner=self.owner).order_by('-timesOpened')

    def getItems(self):
        """return children items."""
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
        """recursively count the items on itself and all subcontainers of it's subcontainers"""
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
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parentItem = models.ForeignKey('self', null=True, on_delete=models.CASCADE, default=None)
    completed_at = models.DateTimeField(null=True, default=None)

    def create_ItemStatementVersion(self):
        current_version_statement_exists = Item.objects.filter(pk=self.pk, owner=self.owner).exists()
        last_version_saved_exists = self.get_versions().exists()

        if current_version_statement_exists and last_version_saved_exists:
            current_version_statement = Item.objects.get(pk=self.pk, owner=self.owner).statement
            last_version_saved_statement = self.get_versions().last()

            if current_version_statement != last_version_saved_statement:
                ItemStatementVersion.objects.get_or_create(statement=current_version_statement, defaults={"created_at" : self.updated_at, "parentItem": self,  "owner":self.owner})

    def save(self, *args, **kwargs):
        """creates ItemStatementVersion objects before saving"""
        self.create_ItemStatementVersion()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.statement

    def get_parentContainer(self):
        """returns parentContainer object as currently instanciated from db"""
        parentContainer_exists = Container.objects.filter(pk=self.parentContainer.pk, owner=self.owner).exists()

        if parentContainer_exists:
            return Container.objects.get(pk=self.parentContainer.pk, owner=self.owner)
        return None
    
    def get_parentItem(self):
        """returns parentItem object as currently instanciated from db"""
        parentItem_exists = Item.objects.filter(pk=self.parentItem.pk, owner=self.owner)

        if parentItem_exists:
            return Item.objects.get(pk=self.parentItem.pk, owner=self.owner)
        return None

    def get_versions(self):
        versions_exist = ItemStatementVersion.objects.filter(parentItem=self, owner=self.owner).exists()
        
        if versions_exist:
            return ItemStatementVersion.objects.filter(parentItem=self, owner=self.owner)
        return None
    
    def toggleDone(self):
        if self.done:
            self.done = False
            self.completed_at = None
        else:
            self.done = True
            self.completed_at = timezone.now()
        self.save()
        
        return self.done


class ItemStatementVersion(models.Model):
    statement = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    parentItem = models.ForeignKey(Item, null=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.statement