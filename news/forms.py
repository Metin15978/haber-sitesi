from django import forms
from .models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','content']

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['news_title', 'news_content', 'news_image', 'category']  # slug alanını kaldırdık

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['news_image'].required = False  #