from django import forms

from car_showroom.common.models import CarComment, CarTestDrive


class SearchCarsByTypeForm(forms.Form):
    TYPE_CHOICES = (
        ('Sports Car', 'Sports Car'),
        ('Pickup', 'Pickup'),
        ('Crossover', 'Crossover'),
        ('Other', 'Other'),
    )

    car_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        required=False,
    )


class CommentCarForm(forms.ModelForm):
    class Meta:
        model = CarComment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'cols': 40,
                    'rows': 2,
                    'placeholder': 'Add comment...'
                },
            ),
        }


class CreateTestDriveForm(forms.ModelForm):
    class Meta:
        model = CarTestDrive
        fields = ('test_drive_date',)


class EditTestDriveForm(forms.ModelForm):
    class Meta:
        model = CarTestDrive
        fields = ('test_drive_date',)


class DeleteTestDriveForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.required = False

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = CarTestDrive
        fields = ('test_drive_date',)
