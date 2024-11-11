import os
from collections import defaultdict

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.shortcuts import render

from .forms import CodeBlocks
from importlib import import_module

from .utils import change_code
import re


def code_mod(request):
    if request.method == 'POST':
        form = CodeBlocks(request.POST)

        if form.is_valid():

            app = form.cleaned_data['apps']
            view = form.cleaned_data['views']
            code_block = form.cleaned_data['code_block']

            print(f"!!!! form is good !!!! -> trying to change code of ({app} - {view})")
            change_code(app=app, view=view, code_block=code_block)
            return JsonResponse({"did": "change"})

#<ul class="errorlist"><li>views<ul class="errorlist"><li>Select a valid choice. hello4 is not one of the available choices.</li></ul></li></ul>
# FIX THIS
        # FOR NOW WE IGNORE

        app = form.cleaned_data['apps']
        code_block = form.cleaned_data['code_block']
        view = re.findall(r'(?:valid choice\.\s)(\w+)', form.errors.__str__())[0]

        print(f"!!!! form is bad :s !!!! -> trying to change code of ({app} - {view})")
        change_code(app=app, view=view, code_block=code_block)
        return render(request, 'code_modifier/code_blocks.html', {'form': form})
        # return JsonResponse({"did": "error", "message": "Form is not valid."})
    else:
        form = CodeBlocks()

    return render(request, 'code_modifier/code_blocks.html', {'form': form})


def get_views_for_app(request):
    return JsonResponse({'views': _get_app_views_names().get(request.GET.get('app_name'), [])})


def _get_app_views_names() -> dict[str, list[str]]:
    app_to_view = defaultdict(list)

    for app_name in set(settings.INSTALLED_APPS) & (set(os.listdir(settings.BASE_DIR))):
        print("APP -0> ", app_name)
        module = import_module(app_name)

        for url_view in (set([el.name for el in module.urls.urlpatterns.__iter__()])) & set(dir(module.views)):
            app_to_view[app_name].append(url_view)
    return app_to_view
