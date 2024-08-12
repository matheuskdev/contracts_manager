from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Party


class PartyListView(ListView):
    model = Party
    template_name = 'party_list.html'
    context_object_name = 'parties'


class PartyDetailView(DetailView):
    model = Party
    template_name = 'party_detail.html'
    context_object_name = 'party'


class PartyCreateView(CreateView):
    model = Party
    template_name = 'party_form.html'
    fields = ['name', 'address', 'email', 'phone']
    success_url = reverse_lazy('party-list')


class PartyUpdateView(UpdateView):
    model = Party
    template_name = 'party_form.html'
    fields = ['name', 'address', 'email', 'phone']
    success_url = reverse_lazy('party-list')


class PartyDeleteView(DeleteView):
    model = Party
    template_name = 'party_confirm_delete.html'
    success_url = reverse_lazy('party-list')
