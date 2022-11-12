from django.forms.widgets import TextInput

class TextRangeInput(TextInput):
    template_name = 'main/text_range.html'
    max_range = 10800
    step = 300

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["max_range"] = self.max_range
        context["widget"]["step"] = self.step
        return context