from .models import Table1
from .serializers import Table1Serializer, Table1AggregateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum


class Table1APIView(APIView):

    def get(self, request):
        query_fields = request.query_params.get('fields', None)
        query_group = request.query_params.get('group', None)
        query_aggregate = request.query_params.get('aggregate', None)
        fields = None
        if query_fields:
            fields = tuple(query_fields.split(','))

        if query_group and query_aggregate:
            table1 = Table1.objects.annotate(
                sum_of_prices=Sum('price'))
            serializer = Table1AggregateSerializer(
                table1, many=True, fields=fields)
        else:
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
