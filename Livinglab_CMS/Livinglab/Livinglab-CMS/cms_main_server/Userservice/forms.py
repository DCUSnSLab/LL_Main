from django import forms
from Management.models import Comment, Comment_media, \
    Content, Content_Description

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
                  'author',
                  'phonenum',
                  'disclosure_status',
                  'confirmation_use_information_status'
                  ]

class AddContentDescriptionForm(forms.ModelForm):
    class Meta:
        model = Content_Description
        fields = ['description',
                  'upload_file',
                  ]
