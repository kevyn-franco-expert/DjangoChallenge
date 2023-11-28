# encoding: utf-8

from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer
from django.db.models import Count
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserRequestHistory
from .permissions import IsSuperuser
# from .services import get_stock_data_http
# from api_service.api_service.my_celery import app
from api_service.my_celery import app

class StockView(APIView):
    """
    Endpoint to allow users to query stocks
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        stock_code = request.query_params.get('q')
        if not stock_code:
            return Response({"error": "Stock code is required"}, status=status.HTTP_400_BAD_REQUEST)

        # stock_data = get_stock_data_http(stock_code)
        # if not stock_data:
        #     return Response({"error": "Stock data not found"}, status=status.HTTP_404_NOT_FOUND)

        result = app.send_task('stocks.tasks.get_stock_data', args=[stock_code])

        try:
            stock_data = result.get(timeout=10)  # Esperar la respuesta hasta un máximo de 10 segundos
        except TimeoutError:
            return Response({"error": "Request timed out"}, status=status.HTTP_408_REQUEST_TIMEOUT)

        stock_data['user_id'] = request.user.id
        UserRequestHistory.objects.create(
            **stock_data
        )
        return Response(stock_data)


class HistoryView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    """
    Returns queries made by current user.
    """
    serializer_class = UserRequestHistorySerializer

    def get_queryset(self):
        return UserRequestHistory.objects.filter(user=self.request.user).order_by('-date')


class StatsView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsSuperuser)
    """
    Allows super users to see which are the most queried stocks.
    """

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        top_stocks_query = UserRequestHistory.objects.values('symbol') \
                               .annotate(times_requested=Count('symbol')) \
                               .order_by('-times_requested')[:5]

        top_stocks = [{"stock": stock['symbol'], "times_requested": stock['times_requested']} for stock in
                      top_stocks_query]

        return Response(top_stocks)

# class StockView(APIView):
#     """
#     Endpoint to allow users to query stocks
#     """
#     def get(self, request, *args, **kwargs):
#         stock_code = request.query_params.get('q')
#         # TODO: Call the stock service, save the response, and return the response to the user
#         return Response()
#
#
# class HistoryView(generics.ListAPIView):
#     """
#     Returns queries made by current user.
#     """
#     queryset = UserRequestHistory.objects.all()
#     serializer_class = UserRequestHistorySerializer
#     # TODO: Filter the queryset so that we get the records for the user making the request.
#
#
# class StatsView(APIView):
#     """
#     Allows super users to see which are the most queried stocks.
#     """
#     # TODO: Implement the query needed to get the top-5 stocks as described in the README, and return
#     # the results to the user.
#     def get(self, request, *args, **kwargs):
#         return Response()
