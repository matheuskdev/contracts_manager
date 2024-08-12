from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . import models, forms


class PartyListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Party
    template_name = 'party_list.html'
    context_object_name = 'parties'
    paginate_by = 10
    permission_required = 'parties.view_party'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class PartyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Party
    template_name = 'party_form.html'
    form_class = forms.PartyForm
    success_url = reverse_lazy('party_list')
    permission_required = 'parties.add_party'


class PartyDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Party
    template_name = 'party_detail.html'
    context_object_name = 'party'
    permission_required = 'parties.view_party'

class PartyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Party
    template_name = 'party_form.html'
    form_class = forms.PartyForm
    success_url = reverse_lazy('party_list')
    permission_required = 'parties.change_party'


class PartyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Party
    template_name = 'party_confirm_delete.html'
    success_url = reverse_lazy('party_list')
    permission_required = 'parties.delete_party'