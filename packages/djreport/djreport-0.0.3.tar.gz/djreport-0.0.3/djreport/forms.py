# dj
from django import forms

# internal
from . import consts


class RenderReportForm(forms.Form):
    """Render Report Form"""

    output_format = forms.ChoiceField(
        choices=consts.OUTPUT_FORMAT_CHOICES, required=False
    )
