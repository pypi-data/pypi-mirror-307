import os

from django import forms
from django.conf import settings

test_code = """
@require_POST
def _(request):
    import random
    vv = random.randint(-10, 0)
    print("CHANGsES") 
    # print("sss:")
    if vv == -6:
        return JsonResponse({"CHANGES": vv})
    return JsonResponse({"CHANGES": f", {vv}"})
"""


class CodeBlocks(forms.Form):
    apps = forms.ChoiceField(
        choices=([("", "Select an App")] + [(el, el) for el in
                                            set(settings.INSTALLED_APPS) & (set(os.listdir(settings.BASE_DIR)))]),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select App",
        required=True,
    )
    views = forms.ChoiceField(
        choices=[("", "Select a View")],
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_views'}),
        label="Select View",
        required=True
    )

    code_block = forms.CharField(
        widget=forms.Textarea(attrs={'name': 'body', 'rows': 10, 'cols': 50, 'class': 'form-control'}),
        label="Code Block",
        max_length=10_000,
        required=True,
        empty_value=test_code

    )
    code_block.initial = test_code

    def clean(self):
        cleaned_data = super().clean()

        app = cleaned_data.get("apps")
        view = cleaned_data.get("views")
        code_block = cleaned_data.get("code_block")
        if not app:
            print("not app in form ", app)
            self.add_error('apps', 'An app must be selected.')
        if not view:
            print("not view in form ", view)
            self.add_error('views', 'A view must be selected.')
        if not code_block:
            print("not code in form ", code_block)
            self.add_error('code_block', 'The code block cannot be empty.')

        return cleaned_data
