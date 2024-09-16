from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from contracts.models import Contract
from parts.models import Part
from folders.models import Folder
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.utils.dateparse import parse_date

class Dashboard(LoginRequiredMixin, View):
    """View for the dashboard page"""
    template_name = "dashboard.html"

    def get(self, request):
        """Get and process data for the dashboard with optional date filters"""
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        context = {
            "username": request.user.username,
            **self.get_contract_data(start_date, end_date),
            "total_addendums": self.get_total_addendums(start_date, end_date),
            "total_evaluations": self.get_total_evaluations(start_date, end_date),
            "total_parts": self.get_total_parts(),
            "total_folders": self.get_total_folders(),
            **self.get_contracts_by_month(start_date, end_date),
            **self.get_total_contract_type(start_date, end_date),
        }
        return render(request, self.template_name, context=context)

    def apply_date_filter(self, queryset, start_date=None, end_date=None):
        """Applies a date range filter to a queryset based on contract start_date."""
        if start_date:
            queryset = queryset.filter(start_date__gte=parse_date(start_date))
        if end_date:
            queryset = queryset.filter(start_date__lte=parse_date(end_date))
        return queryset

    def get_contract_data(self, start_date=None, end_date=None):
        """Retrieve contract-related data with optional date filters"""
        today = timezone.now().date()
        contract_qs = Contract.objects.all()
        contract_qs = self.apply_date_filter(contract_qs, start_date, end_date)

        contract_data = {
            'total_contract': contract_qs.count(),
            'total_contract_approved': contract_qs.filter(status='approved').count(),
            'total_contract_completed': contract_qs.filter(status='completed').count(),
            'total_contract_draft': contract_qs.filter(status='draft').count(),
            'total_contract_canceled': contract_qs.filter(status='canceled').count(),
            'total_contract_renewed': contract_qs.filter(status='renewed').count(),
            'total_contract_expired': contract_qs.filter(end_date__lt=today).count(),
            'total_contract_not_expired': contract_qs.filter(end_date__gte=today).count(),
        }
        return contract_data

    def get_total_contract_type(self, start_date=None, end_date=None):
        """Retrieve contracts type with optional date filters"""
        contract_qs = Contract.objects.all()
        contract_qs = self.apply_date_filter(contract_qs, start_date, end_date)

        contract_type_data = {
            'total_contract_type_service': contract_qs.filter(contract_type='service').count(),
            'total_contract_type_sales': contract_qs.filter(contract_type='sales').count(),
            'total_contract_type_rental': contract_qs.filter(contract_type='rental').count(),
            'total_contract_type_partnership': contract_qs.filter(contract_type='partnership').count(),
        }
        return contract_type_data

    def get_total_addendums(self, start_date=None, end_date=None):
        """Calculate the total number of addendums across all contracts with optional date filters"""
        contract_qs = Contract.objects.all()
        contract_qs = self.apply_date_filter(contract_qs, start_date, end_date)

        return contract_qs.annotate(total_addendums=Count('addendums')).aggregate(Sum('total_addendums'))['total_addendums__sum'] or 0

    def get_total_evaluations(self, start_date=None, end_date=None):
        """Calculate the total number of evaluations across all contracts with optional date filters"""
        contract_qs = Contract.objects.all()
        contract_qs = self.apply_date_filter(contract_qs, start_date, end_date)

        return contract_qs.annotate(total_evaluations=Count('evaluations')).aggregate(Sum('total_evaluations'))['total_evaluations__sum'] or 0

    def get_total_parts(self):
        """Retrieve total parts count"""
        return Part.objects.count()

    def get_total_folders(self):
        """Retrieve total folders count"""
        return Folder.objects.count()

    def get_contracts_by_month(self, start_date=None, end_date=None):
        """Get contract values aggregated by month with optional date filters"""
        contract_qs = Contract.objects.all()
        contract_qs = self.apply_date_filter(contract_qs, start_date, end_date)

        contracts_by_month = (
            contract_qs.annotate(month=TruncMonth('start_date'))
            .values('month')
            .annotate(total_amount=Sum('amount'))
            .order_by('month')
        )

        labels = [contract['month'].strftime('%b-%Y') for contract in contracts_by_month if contract['month']]
        data = [float(contract['total_amount']) for contract in contracts_by_month]

        return {
            "labels": labels,
            "data": data,
        }


class DashboardFilteredData(Dashboard):
    def get(self, request):
        """Retrieve filtered data for chart"""
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        contract_data = self.get_contracts_by_month(start_date, end_date)

        return JsonResponse({
            "labels": contract_data["labels"],
            "data": contract_data["data"]
        })
