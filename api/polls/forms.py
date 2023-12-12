from django import forms

from ckeditor.widgets import CKEditorWidget

from api.polls.models import Poll


class CustomCKEditorWidget(CKEditorWidget):
    def use_required_attribute(self, initial):
        return False

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        if not value:
            return None
        value = value.replace("<p>", "").replace("</p>", "").replace("&#39;", "’").replace("&rsquo;", "’").replace("&nbsp;", "") # noqa
        return value



class PollModelAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CustomCKEditorWidget())

    class Meta:
        model = Poll
        fields = '__all__'