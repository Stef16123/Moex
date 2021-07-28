from .models import Issuer, Security, Price, Portfolio
from rest_framework import serializers


class IssuerSerializer(serializers.ModelSerializer):
    industry_name = serializers.CharField(max_length=150)
    count_securities = serializers.IntegerField()

    class Meta:
        model = Issuer
        fields = ['external_id', 'title', 'industry', 'industry_name', 'count_securities']


class SecuritySerializer(serializers.ModelSerializer):
    average_price = serializers.IntegerField()
    min_price = serializers.IntegerField()
    max_price = serializers.IntegerField()

    class Meta:
        model = Security
        fields = ['issuer', 'title', 'isin', 'code', 'type', 'average_price', 'min_price', 'max_price']


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['date', 'price', 'security']


class PriceCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['count']


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['security', 'count']
