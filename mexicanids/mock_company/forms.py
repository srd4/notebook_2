from django import forms
from .models import Person, PersonDocument
from django.core.exceptions import ValidationError


def file_size(value):
    # a simple size validator function for documents uploaded.
    limit = 3 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 3 MiB.')


class ShortPersonForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))


class FullPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FullPersonForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['placeholder'] = self.fields[i].label

    # extra fields on form that Person model doesn't have and are going to be
    # used to create PersonDocument objects on save() method below.
    passport = forms.FileField(required=False, validators=[file_size])
    identity_document = forms.FileField(required=False, validators=[file_size])
    drivers_license = forms.FileField(required=False, validators=[file_size])
    extra = forms.FileField(required=False, validators=[file_size])

    def clean(self):
        cleaned_data = super().clean()
        document_types = [i[1] for i in PersonDocument.DOC_TYPE_CHOICES]

        if sum(cleaned_data.get(i) == None for i in document_types) == len(document_types):
            raise ValidationError('Must include a valid identification document.')

        return cleaned_data

    def save(self, commit=False):
        instance = super(FullPersonForm, self).save(commit=False)
        document_types = [i[1] for i in PersonDocument.DOC_TYPE_CHOICES]
        # Separating Person fields cleaned data from those of PersonDocuments to create objects separately.
        person_fields = {x: self.cleaned_data[x] for x in self.cleaned_data if x not in document_types}

        # Update or create a person, fetch by email and update rest.
        a_person, created = Person.objects.update_or_create(email=person_fields['email'], defaults=person_fields)

        for i in document_types:
            if self.cleaned_data[i] != None:
                # Create a PersonDocument object for every file uploaded, assigning it to above Person.
                person_document, created = PersonDocument.objects.get_or_create(person=a_person, file=self.cleaned_data[i])
                # Add document type attribute to this PersonDocument object.
                person_document.document_type = document_types.index(i)
                person_document.save()
        
        if commit:
            instance.save()

        return instance
