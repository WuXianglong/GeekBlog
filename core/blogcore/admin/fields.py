from django import forms


class NotValidateChoiceField(forms.ChoiceField):

    def validate(self, value):
        return


class NotValidateMultipleChoiceField(forms.MultipleChoiceField):

    def validate(self, value):
        return
