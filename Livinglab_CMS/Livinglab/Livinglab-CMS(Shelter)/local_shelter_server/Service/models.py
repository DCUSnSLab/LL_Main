from django.db import models

class Drawing(models.Model):

    path = models.CharField(max_length=200, null=True)
    createDate = models.DateTimeField(auto_now_add=True, null=True)  # 등록일자