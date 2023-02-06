from django import forms
from .models import Shelter, Shelter_media, \
Advertisement, Advertisement_media

class ShelterRegisterForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = ['title',
                  'shelter_description',
                  'add_states',
                  'add_city',
                  'add_town',
                  'add_last',
                  ]

class ShelterMediaForm(forms.ModelForm):
    class Meta:
        model = Shelter_media
        fields = ['shelter_profile']

class AdRegisterForm(forms.ModelForm):
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

class AdMediaRegisterForm(forms.ModelForm):
    class Meta:
        model = Advertisement_media
        fields = [
            'content'
        ]
