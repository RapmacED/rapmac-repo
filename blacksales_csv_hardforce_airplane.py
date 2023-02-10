import airplane
from typing_extensions import Annotated
import io
import csv
import urllib.request
import pandas as pd

@airplane.task(
    slug="blacksales_csv_hardforce",
    name="BlackSales csv hardforce",
)
def blacksales_csv_hardforce(
    emails_list: Annotated[
        airplane.File,
        airplane.ParamConfig(
            slug="emails_list",
            name="emails_list",
        ),
    ],
):
    #print(emails_list['url'])
    url = emails_list.url
    response = urllib.request.urlopen(url)
    df = pd.read_csv(io.TextIOWrapper(response))
    #csv_file = csv.reader(io.TextIOWrapper(response))
    print(df)

    # You can return data to show output to users.
    # Output documentation: https://docs.airplane.dev/tasks/output
    return df