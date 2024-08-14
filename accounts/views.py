from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class Home(LoginRequiredMixin, View):
    template_name = 'home.html'
    
    def get(self, request):
        user = self.request.user
        context = { 'username': user.username}
        return render(request, self.template_name, context=context)