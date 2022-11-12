from django.forms import ModelForm
from django.utils.translation import gettext as _

from main.models import Visit, Service

from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from main.widgets import TextRangeInput


class ClientVisitForm(ModelForm):
    class Meta:
        model = Visit
        exclude = ['client']
        widgets = {
            'date_time' : DateTimePickerInput(),
        }


class MasterVisitForm(ModelForm):
    class Meta:
        model = Visit
        fields = '__all__'
        widgets = {
            'date_time' : DateTimePickerInput(),
        }


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {
            "duration": TextRangeInput(),
        }
