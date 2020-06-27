from django import forms

class WordSearchForm(forms.Form):
	word = forms.CharField(label='Search a word', max_length = 100)

class WordChooseForm(forms.Form):

    def __init__(self, word_choices, *args, **kwargs):
        super(WordChooseForm, self).__init__(*args, **kwargs)
        self.fields['word_id'].choices = word_choices

    word_id = forms.ChoiceField(choices=(), label='Choose a word', required=True)