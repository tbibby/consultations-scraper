from bs4 import BeautifulSoup
from dateutil import parser
import re

# Define the filename
filename = 'cork-county-fragments.txt'
# start date and end date for 2, 8, 9, 18, 19, 20, 23, 26, 27, 32, 33, 34
#date_pattern = r'From (.*?) to (.*?)(?:\.|$)'
# matches start date and end date for 19, 20, 23, 26, 27, 32, 33, 34
#date_pattern = r'from (.*?) to (.*?)inclusive'

#from 9am on Friday 19th July until 5pm Thursday 15th August 2024 inclusive
# 21, 22, 24, 25, 28, 29, 30, 31
date_pattern = r'from (.*?) until (.*?)inclusive'

#from</span></span>&nbsp;<span><span>10/12/2021</span></span>&nbsp;during public opening hours
#before 5.00pm on 28/01/2022.
date_pattern = r'from (.*?) during public .*? before (.*?).'

# matches 34 end date
#date_pattern = r'on, or before, (.*?)(?:\.|$)'
# from Thursday 11th July to Monday 12th August 2024 inclusive

#no later than 4.00pm on 16th September 2022.
# matches end dates for 1, 7, 8, 9
#date_pattern = r'no later than (\d{1,2}\.\d{2}(?:am|pm) on \d{1,2}(?:st|nd|rd|th) \w+ \d{4})'

#no later than 4.00pm on Friday, 16th September 2022.
# matches end date for 2
#date_pattern = r'no later than (\d{1,2}\.\d{2}(?:am|pm) on \w{1,9}, \d{1,2}(?:st|nd|rd|th) \w+ \d{4})'

# and must reach the Senior Engineer on or before 4pm on Friday, 12th August 2022.
#end date for 3, 4
# date_pattern = r'and must reach the Senior Engineer on or before (\d{1,2}(?:am|pm) on \w{1,9}, \d{1,2}(?:st|nd|rd|th) \w+ \d{4})'

# may be made on or before 4pm on Monday 25/07/2022 
# end date on 5
#date_pattern = r'on or before (\d{1,2}(?:am|pm) on \w{1,9} \d{1,2}/\d{1,2}/\d{4})'

# from Friday 6th-May-2022 until Friday 3rd-June-2022.
# start and end for 3, 4, 6, 10
#date_pattern = r'from (.*?) until (.*?)(?:\.|$)'

# from 5pm Thursday 15th August 2024 inclusive to 9am on Friday 19th July
# matches nothing
#date_pattern = r'from (.*?) inclusive until (.*?)(?:\.|$)'

#on or before 5 pm on Thursday 4th August 2022.
#end dates for 3, 4, 10, 12, 18, 20, 21, 22, 24, 25, 26, 28, 29, 30, 31
#error on 6
#date_pattern = r'on or before (.*?)(?:\.|$)'

#11
# from&nbsp;<strong>Monday 7th&nbsp;February 2022</strong>&nbsp;until&nbsp;<strong>Friday 25th&nbsp;March 2022</strong>.
#date_pattern = r'No later than 4.00pm on (.*?)(?:\.|$)'

# on or before 4pm on Friday 8th&nbsp;April 2022</strong>.
# 3, 4, 6, 10, 12
#date_pattern = r'on or before 4pm on (.*?)(?:\.|$)'

# No later than 4.00pm on Monday 21st&nbsp;March, 2022.
# 13
#date_pattern = r'No later than 4.00pm on (.*?)(?:\.|$)'

# Open and read the file
with open(filename, 'r') as file:
    content = file.read()

# Split the content by the separator
fragments = content.split('-----')

# Loop over each fragment
for index, fragment in enumerate(fragments):
    # Strip whitespace and check if the fragment is not empty
    fragment = fragment.strip()
    if fragment:
        # Parse the fragment with BeautifulSoup
        soup = BeautifulSoup(fragment, 'html.parser')
        # Get the raw text
        raw_text = soup.get_text()
        #if index+1 == 11:
        #    print(raw_text)
        # Search for the date pattern in the raw text
        match = re.search(date_pattern, raw_text, re.IGNORECASE)
        if match:
            start_date_str = match.group(1).strip()
            end_date_str = match.group(2).strip()

            try:
                # Parse the date strings to date objects
                start_date = parser.parse(start_date_str, fuzzy=True)
                end_date = parser.parse(end_date_str, fuzzy=True)

                print(f"Fragment {index + 1}:\nStart Date: {start_date}\nEnd Date: {end_date}\n")
                #print(f"Fragment {index + 1}:\nEnd Date: {end_date}\n")
                #print(f"Fragment {index + 1}:\nEnd Date: {start_date}\n")
            except ValueError as e:
                print(f"Fragment {index + 1}:\nError parsing dates: {e} {start_date_str} \n")
        else:
            print(f"Fragment {index + 1}:\nNo date range found.\n")