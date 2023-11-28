import csv
from datetime import datetime
from io import StringIO


def parse_csv_response(response):
    csv_file = StringIO(response)
    reader = csv.DictReader(csv_file)

    processed_data = []
    for row in reader:
        datetime_str = f"{row['Date']} {row['Time']}"
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

        new_row = {key.lower(): value for key, value in row.items() if key not in ['Date', 'Time', 'Volume']}
        new_row['date'] = datetime_obj

        processed_data.append(new_row)

    return processed_data[0] if processed_data else None
