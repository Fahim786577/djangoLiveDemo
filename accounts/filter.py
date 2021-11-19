from django.db.models import fields
import django_filters
from django_filters.filters import DateFilter
from .models import *
class Orderfilter(django_filters.FilterSet):
    startdate = DateFilter(field_name='datecreated',lookup_expr='gte',label='Start Date')
    enddate = DateFilter(field_name='datecreated',lookup_expr='lte',label='End Date')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'datecreated']