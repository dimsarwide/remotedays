Remote Work Assignments Calendar

This Python script generates remote work assignments for a team of seven people over a specified month. It randomly assigns a given number of remote work days per person per week, ensuring fairness and avoiding consecutive remote days for any individual.
Getting Started

To use this script, ensure you have Python installed on your system. Clone this repository and run the script with the required arguments.

bash

python main.py -y <year> -m <month> -r <remote_days>

Arguments

    -y, --year: Year of the calendar (default: current year)
    -m, --month: Month of the calendar (default: current month)
    -r, --remote_days: Number of remote days per person per week (default: 2)

Example

bash

python main.py -y 2024 -m 6 -r 2

Dependencies

    calendar: Python module for calendar-related functions
    random: Python module for random number generation
    argparse: Python module for command-line argument parsing
    datetime: Python module for manipulating dates and times

Authors

    Dimitris Sarantakis

License

This project is licensed under the MIT License - see the LICENSE.md file for details.
