from .models import Table1
from .serializers import Table1Serializer, Table1AggregateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Avg, Min, Max, Count


class Table1APIView(APIView):

    def get(self, request):
        query_fields = request.query_params.get('fields', None)
        query_group = request.query_params.get('group', None)
        query_aggregate = request.query_params.get('aggregate', None)
        fields = None

        aggregate_tupple = ("sum", "avg", "count", "min", "max")
        groups_tupple = ("userid", "uploaded_time", "city", "price",
                         "year", "county_name", "state_code", "state_name")

        if query_group and query_aggregate and query_group in groups_tupple and query_aggregate in aggregate_tupple:

            if query_aggregate == "sum":
                table1 = Table1.objects.values(
                    query_group).annotate(sum_of_prices=Sum('price'))
                fields = (query_group, "sum_of_prices")
            elif query_aggregate == "avg":
                table1 = Table1.objects.values(
                    query_group).annotate(avg_of_prices=Avg('price'))
                fields = (query_group, "avg_of_prices")
            elif query_aggregate == "count":
                table1 = Table1.objects.values(query_group).annotate(
                    count_of_prices=Count('price'))
                fields = (query_group, "count_of_prices")
            elif query_aggregate == "min":
                table1 = Table1.objects.values(
                    query_group).annotate(min_of_prices=Min('price'))
                fields = (query_group, "min_of_prices")
            else:
                table1 = Table1.objects.values(
                    query_group).annotate(max_of_prices=Max('price'))
                fields = (query_group, "max_of_prices")

            serializer = Table1AggregateSerializer(
                table1, many=True, fields=fields)
        else:
            if query_fields:
                fields = tuple(query_fields.split(','))
            table1 = Table1.objects.all()
            serializer = Table1Serializer(table1, many=True, fields=fields)
        return Response(serializer.data)

    def post(self, request):
        serializer = Table1Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Table1Details(APIView):

    def get_object(self, id):
        try:
            return Table1.objects.get(id=id)
        except Table1.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        table1 = self.get_object(id)
        serializer = Table1Serializer(table1)
        return Response(serializer.data)

    def put(self, request, id):
        table1 = self.get_object(id)
        serializer = Table1Serializer(table1, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        table1 = self.get_object(id)
        table1.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
