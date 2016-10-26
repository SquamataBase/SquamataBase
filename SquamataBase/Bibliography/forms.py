from django import forms
from dal import autocomplete
from .models import *

class JournalArticleForm(forms.ModelForm):
    class Meta:
        model = JournalArticle
        fields = ('__all__')
        widgets = {
            'journal': autocomplete.ModelSelect2(
                url = 'journal-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for journals . . .',
                    #'data-minimum-input-length': 2,
                },
            ),
            'title': forms.Textarea(attrs={'rows': 1, 'cols': 30})
        }


class BookChapterForm(forms.ModelForm):
    class Meta:
        model = BookChapter
        fields = ('__all__')
        widgets = {
            'book': autocomplete.ModelSelect2(
                url = 'book-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for books . . .',
                    'data-minimum-input-length': 2,
                },
            ),
        }
        
        
class ContributionForm(forms.ModelForm):
    class Meta:
        model = BookChapter
        fields = ('__all__')
        widgets = {
            'person': autocomplete.ModelSelect2(
                url = 'person-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for people . . .',
                    'data-minimum-input-length': 2,
                },
            ),
        }
        