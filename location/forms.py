from django.forms import ModelForm
from .models import Place, Post

class CategorisePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'second_category', 'third_category')
