from django.shortcuts import render
from .models import Issuer, Security, Price, Portfolio
from rest_framework import viewsets
from .serializers import IssuerSerializer, SecuritySerializer, PriceSerializer, PortfolioSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Min, Max, Sum, Count, F, ExpressionWrapper, FloatField


def home(request):
    return render(request, 'moex/home.html')


class IssuerView(viewsets.ModelViewSet):
    queryset = Issuer.objects.all()
    serializer_class = IssuerSerializer


class SecurityView(viewsets.ModelViewSet):
    queryset = Security.objects.all()
    serializer_class = SecuritySerializer

    def get_queryset(self):
        return Security.objects.annotate(
            average_price=Avg('prices__price'),
            min_price=Min('prices__price'),
            max_price=Max('prices__price')
        )


class PriceView(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class IssuerView(viewsets.ModelViewSet):
    queryset = Issuer.objects.all()
    serializer_class = IssuerSerializer

    def get_queryset(self):
        return Issuer.objects.annotate(
            industry_name=F('industry__name'),
            count_securities=Count('securities')
        )


class PortfolioView(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    @action(methods=['get'], detail=False)
    def get_statistic(self, request, pk=None):
        count__sum = Portfolio.objects.aggregate(Sum('count'))['count__sum']

        industry_statistic = Portfolio.objects\
            .values(industry=F('security__issuer__industry__name'))\
            .annotate(
                avg_price=Sum('security__prices__price') / Count('security__prices'),
                different_securities=Count('security_id', distinct=True),
                bough_securities=Sum('count', distinct=True),
                percent_bought_securities=ExpressionWrapper(
                    (F('bough_securities') * 1.0 / count__sum * 100), output_field=FloatField()))

        for statistic in industry_statistic:
            statistic['percent_bought_securities'] = str(statistic['percent_bought_securities']) + '%'
        return Response(dict(statistic=industry_statistic))
