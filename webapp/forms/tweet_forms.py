from django import forms

from webapp.models.tweet import Tweet


class CreateTweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = Tweet.fields()

    message = forms.CharField(label='Message', widget=forms.Textarea)
    image = forms.ImageField(label='Image', required=False)
