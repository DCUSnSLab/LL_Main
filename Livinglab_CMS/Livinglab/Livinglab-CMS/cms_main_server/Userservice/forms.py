from django import forms
from Management.models import Comment, Comment_media, \
    Content, Content_Description, Advertisement, Advertisement_media

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',
                  'email',
                  'boardType'
                  ]

class AddCommentMediaForm(forms.ModelForm):
    class Meta:
        model = Comment_media
        fields = ['image',
                  ]

class UploadContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title',
                  'email',
                  ]

class UploadAdForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = [
            'name',
            'adType',
            'company',
            'advertiser',
            'email',
            'phone',
        ]

class UploadAdMediaForm(forms.ModelForm):
    class Meta:
        model = Advertisement_media
        fields = [
            'content'
        ]

class AddContentDescriptionForm(forms.ModelForm):
    class Meta:
        model = Content_Description
        fields = ['description',
                  'upload_file',
                  ]
