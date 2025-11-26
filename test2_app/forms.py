from django.forms import ModelForm
from .models import Test2News, Comment

class Test2NewsForm(ModelForm):
    class Meta:
        
        model = Test2News
        
        fields = ['category', 'title', 'post', 'image1', ]

class PhotoEditForm(Test2NewsForm):
    class Meta(Test2NewsForm.Meta):
        
        fields = ['category', 'title', 'post', 'image1', ]

class CommentForm(ModelForm):
    class Meta:
        
        model = Comment
        
        fields = ['text', ]