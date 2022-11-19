from datetime import date, datetime

t = date.today()
print(t)
date1 = date(2023, 5, 5)
print(date1)

if t < date1:
    print('yes')

with open('tasks.txt', 'r') as f:
    due_dates = []
    for task in f.readlines():
        tasks = task.split(';')
        print(tasks)
        due_dates.append(tasks[3])
    print(due_dates)

one = due_dates[0].split('-')
print(one)
day = int(one[2])
month = int(one[1])
print(month)
year = int(one[0])

due_date = date(year, month, day)
print(due_date)

if due_date < t:
    print('overdue')
else:
    print('on schedule')

print(type(t))

yes = []
print(len(yes))
