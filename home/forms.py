from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "id": "title-input",
                    "placeholder": "Add title here...",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "id": "md-content",
                    "placeholder": "Add markdown here...",
                }
            ),
        }
