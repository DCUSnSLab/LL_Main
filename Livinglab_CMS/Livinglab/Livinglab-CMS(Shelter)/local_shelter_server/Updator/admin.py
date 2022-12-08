from django.contrib import admin
from .models import Shelter, Community, Daily_Board, Issue_Board, Comment, Comment_media,\
Advertisement, Advertisement_media, Content, Content_Description


admin.site.register(Shelter)
admin.site.register(Community)
admin.site.register(Daily_Board)
admin.site.register(Issue_Board)
admin.site.register(Comment)
admin.site.register(Comment_media)
admin.site.register(Advertisement)
admin.site.register(Advertisement_media)
admin.site.register(Content)
admin.site.register(Content_Description)

