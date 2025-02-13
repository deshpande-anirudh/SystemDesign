from croniter import croniter
from datetime import datetime

# Current job execution details
# [minute_of_hour] [hour_of_day] [day_of_month] [Month_of_year] [day_of_week]
cron_expression = "0 7 * 3 FRI"  # Run a job every monday
current_due_at = datetime.utcnow()

# Calculate the next execution time
next_due_at = croniter(cron_expression, current_due_at).get_next(datetime)
print(next_due_at)

for _ in range(10):
    next_due_at = next(croniter(cron_expression, next_due_at).all_next(datetime))
    print(next_due_at)
