import csv
import random
from datetime import datetime, timedelta

start_date = datetime(2025, 1, 1, 1,0,0)
end_date = datetime(2025, 1, 1, 1, 5, 0)

def get_char():
    return 'U' + str(random.randint(1, 10000))

with open('./input/input.csv', 'a') as input_csv:
    writer = csv.writer(input_csv)
    writer.writerow(['ad_id', 'click_time', 'user_id'])
    for _ in range(1_000_000):
        date = start_date + timedelta(seconds=random.randint(1, int((end_date-start_date).total_seconds()) ))
        user = random.choice(
            ['A', 'B', get_char()]
        )
        writer.writerow(
            [
                f"ad{random.randint(1, 100)}",
                date,
                user
            ]
        )