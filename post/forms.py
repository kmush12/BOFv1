from django import forms

from .models import Post

class AddPostForm(forms.ModelForm):
    content = forms.CharField(label='',
                              widget=forms.Textarea(attrs={
                                  'rows': '5',
                                  'placeholder': 'Napisz coś :D'
                              }))
    photo = forms.ImageField(label='', required=False)

    class Meta:
        model = Post
        fields = ('content', 'photo')