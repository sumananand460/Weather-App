from django import forms


class CityForm(forms.Form):
    city = forms.CharField(
        label='City',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter city name, e.g. Bhubaneswar',
            'class': 'city-input',
        }),
    )
