from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse


class LoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("You don't have permissions")
        return super().dispatch(request, *args, **kwargs)