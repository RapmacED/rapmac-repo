import airplane
from typing_extensions import Annotated
import csv
import io
import urllib.request


@airplane.task(
    slug="hardforce_blacksales_csv",
    name="Hardforce BlackSales CSV",
    description="Check if the users in a csv files are registered users of BlackSales.",
)
def hardforce_blacksales_csv(
    emails_list: Annotated[
        airplane.File,
        airplane.ParamConfig(
            slug="emails_list",
            name="Emails list",
            description="Column named 'email' containing all emails to test.",
        ),
    ] = "upl20230210zqo136r21v9",
):
    csv_file = csv.reader(io.TextIOWrapper(emails_list))
    for row in csv_file:
        print(row)
    return True
    """data = [
        {"id": 1, "name": "Gabriel Davis", "role": "Dentist"},
        {"id": 2, "name": "Carolyn Garcia", "role": "Sales"},
        {"id": 3, "name": "Frances Hernandez", "role": "Astronaut"},
        {"id": 4, "name": "Melissa Rodriguez", "role": "Engineer"},
        {"id": 5, "name": "Jacob Hall", "role": "Engineer"},
        {"id": 6, "name": "Andrea Lopez", "role": "Astronaut"},
    ]

    # Sort the data in ascending order by name.
    data = sorted(data, key=lambda u: u["name"])

    # You can return data to show output to users.
    # Output documentation: https://docs.airplane.dev/tasks/output
    return data"""
