from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from contracts.models import Contract
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from parts.models import Part


class Dashboard(LoginRequiredMixin, View):
    """ View for the dashboard page"""

    template_name = "dashboard.html"

    def get(self, request):
        """ Get and process data for the dashboard """

        user = request.user
        today = timezone.now().date()
        contract = Contract.objects
        contract_data = {
            'total_contract': contract.count(),
            'total_contract_approved': contract.filter(status='approved').count(),
            'total_contract_completed': contract.filter(status='completed').count(),
            'total_contract_draft': contract.filter(status='draft').count(),
            'total_contract_canceled': contract.filter(status='canceled').count(),
            'total_contract_renewed': contract.filter(status='renewed').count(),
            'total_contract_expired': contract.filter(end_date__lt=today).count(),
            'total_contract_not_expired': contract.filter(end_date__gte=today).count(),
        }

        total_addendums = sum(contract.addendums.count() for contract in Contract.objects.all())
        total_evaluations = sum(contract.evaluations.count() for contract in Contract.objects.all())

        total_parts = Part.objects.count()
        # Agregação de valores de contratos por mês
        contracts_by_month = (
            Contract.objects.annotate(month=TruncMonth('start_date'))
            .values('month')
            .annotate(total_amount=Sum('amount'))
            .order_by('month')
        )

        labels = [contract['month'].strftime('%Y-%m') for contract in contracts_by_month]
        data = [float(contract['total_amount']) for contract in contracts_by_month]

        context = {
            "username": user.username,
            **contract_data,
            "total_addendums": total_addendums,
            "total_evaluations": total_evaluations,
            "total_parts": total_parts,
            "labels": labels,
            "data": data,
        }

        return render(request, self.template_name, context=context)
