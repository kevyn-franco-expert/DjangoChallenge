# encoding: utf-8

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import parse_csv_response


class StockView(APIView):
    """
    Receives stock requests from the API service.
    """

    def get(self, request, *args, **kwargs):
        stock_code = request.query_params.get('stock_code')
        if not stock_code:
            return Response({"error": "Stock code is required"}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(f"https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcvn&h&e=csv")
        if response.status_code != 200:
            return Response({"error": "Error fetching stock data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Parsear y devolver respuesta
        stock_data = parse_csv_response(response.text)
        return Response(stock_data)
