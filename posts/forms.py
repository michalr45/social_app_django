from django import forms
from .models import Post, Comment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'placeholder': 'Enter text'})}


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
