from django.forms import ModelForm, SplitDateTimeWidget
from main.models import Visit
from bootstrap_datepicker_plus.widgets import DateTimePickerInput



class ClientVisitForm(ModelForm):
    class Meta:
        model = Visit
        exclude = ['client']
        widgets = {
            'date_time' : DateTimePickerInput()
        }



class MasterVisitForm(ModelForm):
    class Meta:
        model = Visit
        fields = '__all__'
        widgets = {
            'date_time' : DateTimePickerInput()
        }