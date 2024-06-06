import calendar
import random
import argparse
import datetime

# List of 7 people
names = ['Τσίκα', 'Μαραγκός', 'Σαραντάκης', 'Δώρης', 'Καραογλάνης', 'Χουάν']

def assign_weekly_remote_days(names, previous_friday_remotes, remote_days_per_person):
    days = ['Δευτέρα', 'Τρίτη', 'Τετάρτη', 'Πέμπτη', 'Παρασκευή']
    assignments = {name: [] for name in names}

    while not all(len(assignments[name]) >= remote_days_per_person for name in names):
        for day in days:
            available_names = [name for name in names if len(assignments[name]) < remote_days_per_person]
            if day == 'Δευτέρα':
                available_names = [name for name in available_names if name not in previous_friday_remotes]
            if len(available_names) < len(names) - remote_days_per_person:
                selected_names = available_names
            else:
                selected_names = random.sample(available_names, len(names) - remote_days_per_person)
            for name in selected_names:
                if len(assignments[name]) >= remote_days_per_person:
                    continue
                if day not in assignments[name]:
                    assignments[name].append(day)
                if len([name for name in names if len(assignments[name]) < remote_days_per_person]) >= 2:
                    break

    # Ensure no one has remote on both Δευτέρα and Τρίτη or both Πέμπτη and Παρασκευή
    for name in names:
        if 'Δευτέρα' in assignments[name] and 'Τρίτη' in assignments[name]:
            assignments[name].remove('Τρίτη')
            possible_days = [day for day in days if day not in assignments[name] and day not in ['Δευτέρα', 'Τρίτη']]
            if possible_days:
                new_day = random.choice(possible_days)
                assignments[name].append(new_day)
        if 'Πέμπτη' in assignments[name] and 'Παρασκευή' in assignments[name]:
            assignments[name].remove('Παρασκευή')
            possible_days = [day for day in days if day not in assignments[name] and day not in ['Πέμπτη', 'Παρασκευή']]
            if possible_days:
                new_day = random.choice(possible_days)
                assignments[name].append(new_day)
    
    return assignments

def print_month_calendar(year, month, weekly_assignments):
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)
    days_of_week = ['Δευτέρα', 'Τρίτη', 'Τετάρτη', 'Πέμπτη', 'Παρασκευή', 'Σάββατο', 'Κυριακή']
    
    # Create a reverse mapping of day names to indices
    day_indices = {day: i for i, day in enumerate(days_of_week)}
    
    months_in_greek = {
    "January": "Ιανουάριος",
    "February": "Φεβρουάριος",
    "March": "Μάρτιος",
    "April": "Απρίλιος",
    "May": "Μάιος",
    "June": "Ιούνιος",
    "July": "Ιούλιος",
    "August": "Αύγουστος",
    "September": "Σεπτέμβριος",
    "October": "Οκτώβριος",
    "November": "Νοέμβριος",
    "December": "Δεκέμβριος"
}

    # Print the formatted table
    print(f"Μέρες remote για {months_in_greek[calendar.month_name[month]]} {year}:\n")

    for week_index, week in enumerate(month_days):
        remote_by_day = {day: [] for day in week if day != 0}

        if week_index < len(weekly_assignments):
            assignments = weekly_assignments[week_index]

            # Populate the dictionary with assignments
            for name, days in assignments.items():
                for day_name in days:
                    day_idx = day_indices[day_name]
                    if week[day_idx] != 0:
                        remote_by_day[week[day_idx]].append(name)

        for day in week:
            if day == 0:
                continue
            day_name = days_of_week[week.index(day)]
            names_list = ', '.join(remote_by_day[day])
            print(f"{day}/{month} {day_name}\t{names_list}")
        print()  # Separate each week with an empty line

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate remote work assignments")
    parser.add_argument("-y", "--year", type=int, default=datetime.date.today().year, help="Year of the calendar (default: current year)")
    parser.add_argument("-m", "--month", type=int, default=datetime.date.today().month, help="Month of the calendar (default: current month)")
    parser.add_argument("-r", "--remote_days", type=int, default=2, help="Number of remote days per person per week (default: 2)")
    args = parser.parse_args()

    year = args.year
    month = args.month
    remote_days_per_person = args.remote_days
    if remote_days_per_person < 0 or remote_days_per_person > 4:
        if remote_days_per_person == 5:
            print("Στα όνειρα σου")
        else:
            print("Λανθασμένες μέρες remote")
        exit();

    # Seed the random number generator based on the month and year
    random.seed(year * 100 + month)

    # Initialize previous Παρασκευή remotes as empty for the first week
    previous_friday_remotes = []

    # Assign remote days for each week
    weekly_remote_assignments = []
    for week in range(5):  # Assuming up to 5 weeks in a month
        assignments = assign_weekly_remote_days(names, previous_friday_remotes, remote_days_per_person)
        weekly_remote_assignments.append(assignments)
        previous_friday_remotes = [name for name, days in assignments.items() if 'Παρασκευή' in days]

    # Print the calendar for a specific month and year
    print_month_calendar(year, month, weekly_remote_assignments)

