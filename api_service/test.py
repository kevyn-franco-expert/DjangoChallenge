from api_service.my_celery import app

result = app.send_task('stocks.tasks.get_stock_data', args=['aapl.us'])
stock_data = result.get(timeout=10)