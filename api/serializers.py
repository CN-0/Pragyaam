from rest_framework import serializers
from .models import Table1


class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class Table1Serializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Table1
        fields = "__all__"


class Table1AggregateSerializer(DynamicFieldsModelSerializer):
    sum_of_prices = serializers.DecimalField(10, 2)
    avg_of_prices = serializers.DecimalField(10, 2)
    count_of_prices = serializers.DecimalField(10, 2)
    max_of_prices = serializers.DecimalField(10, 2)
    min_of_prices = serializers.DecimalField(10, 2)

    class Meta:
        model = Table1
        fields = ("userid", "uploaded_time", "city", "price",
                  "year", "county_name", "state_code", "state_name", "sum_of_prices", "avg_of_prices", "count_of_prices", "max_of_prices", "min_of_prices")
