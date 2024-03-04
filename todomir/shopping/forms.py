from django import forms


class NewItemForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=255)


class ItemIDForm(forms.Form):
    item_id = forms.IntegerField()
