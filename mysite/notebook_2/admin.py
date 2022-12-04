from django.contrib import admin
from .models import Container, Item, ItemStatementVersion, Tag

# Register your models here.

admin.site.register(Container)
admin.site.register(Item)
admin.site.register(ItemStatementVersion)
admin.site.register(Tag)