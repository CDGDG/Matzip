from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import View
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout

from user.forms import UserForm

class Join(View):
    def get(self, request: HttpRequest):
        form = UserForm()

        context = {'form': form}
        return render(request, 'user_join.html', context)

    def post(self, request: HttpRequest):
        context = {}

        form = UserForm(request.POST)
        
        if form.is_valid():
            form.save()
            context['form_is_valid'] = True
        else:
            context['form_is_valid'] = False
            context['html_form'] = render_to_string('includes/partial_user_form.html', {'form': form})

        return JsonResponse(context)



                