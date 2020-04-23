from django import forms

class SearchForm(forms.Form):
    subreddit = forms.CharField(label='What subreddit?', max_length=256)
    search_string = forms.CharField(
        label='Search terms?',
        widget = forms.TextInput(
            attrs={'placeholder': 'Comma, separated, list, of, search, terms'}),
        max_length=512)
