from django import forms

from car_showroom.cars.models import Car


class CarBaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CarBaseForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['size'] = 30

    class Meta:
        model = Car
        fields = ('type', 'model', 'year_of_production', 'price', 'horse_power', 'image_url', 'description')

    widgets = {
        'description': forms.TextInput(attrs={'rows': 5, 'cols': 15}),
    }


class CarDetailsForm(CarBaseForm):
    pass


class CarCreateForm(CarBaseForm):
    pass


class CarEditForm(CarBaseForm):
    pass


class CarDeleteForm(CarBaseForm):
    disabled_fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.required = False

    def save(self, commit=True):
        self.instance.delete()
        return self.instance
