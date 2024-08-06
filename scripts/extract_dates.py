import re
from bs4 import BeautifulSoup
from dateutil import parser
from dateutil.relativedelta import relativedelta
import pytz
from datetime import datetime, timedelta

def analyse_text_for_earliest_and_last_date(textToAnalyse):
    # Define the timezone
    dublin_tz = pytz.timezone('Europe/Dublin')

    # Current date
    current_date = datetime.now(dublin_tz)
    # Regular expressions
    month_regex = r'(\d+(?:st|nd|rd|th)?)\s*[-_,]?\s*(?:of\s*)?[-_,]?\s*(January|February|March|April|May|June|July|August|September|October|November|December)\s*[-_,]?\s*(\d{4}|\d{2})'
    abbrev_month_regex = r'(\d+(?:st|nd|rd|th)?)\s*[-_,]?\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*[-_,]?\s*(\d{4}|\d{2})'
    date_regex = r'(\d{1,2})[_./](\d{1,2})[_./](\d{2}|\d{4})'

    # Initialize the list for the current section
    dates_found = []

    # Match full month names and abbreviations
    month_matches = re.findall(month_regex, textToAnalyse)
    abbrev_matches = re.findall(abbrev_month_regex, textToAnalyse)
    
    # Combine matches
    for match in month_matches + abbrev_matches:
        number_before = match[0]
        month_name = match[1]
        number_after = match[2]
        dates_found.append(f"{number_before} {month_name} {number_after}")

    # Match dd/mm/yy or dd/mm/yyyy dates
    date_matches = re.findall(date_regex, textToAnalyse)
    for day, month, year in date_matches:
        dates_found.append(f"{day}/{month}/{year}")
    #try and get proper dates from the strings found with the regexes
    converted_dates = [parser.parse(date, fuzzy=True).astimezone(dublin_tz) for date in dates_found]
    #toss out the dupes
    unique_dates = set(converted_dates)
    if len(unique_dates) == 1:
        unique_date = next(iter(unique_dates))  # Get the single unique date
    
        # Check if the unique date is less than a week after the current date
        if unique_date < current_date or (current_date <= unique_date < current_date + timedelta(weeks=1)):
            earliest = unique_date - relativedelta(months=1)
        else:
            earliest = dublin_tz.localize(datetime.combine(current_date, datetime.min.time().replace(hour=9)))

        latest = unique_date.replace(hour=16, minute=0, second=0, microsecond=0).astimezone(dublin_tz)
        return (earliest.date(), latest.date())
        #print(f"Section {section}: Earliest: {earliest.date()}, Latest: {latest.date()}")
    elif len(unique_dates) > 1:
        # Print the earliest and latest dates
        earliest = min(converted_dates).replace(hour=9, minute=0, second=0, microsecond=0).astimezone(dublin_tz)
        latest = max(converted_dates).replace(hour=16, minute=0, second=0, microsecond=0).astimezone(dublin_tz)
        return (earliest.date(), latest.date())
        #print(f"Section {section}: Earliest: {earliest.date()}, Latest: {latest.date()}")

# Test this function below
# Open the file and read its content
# with open('cork-county-fragments.txt', 'r', encoding='utf-8') as file:
#     text = file.read()

# # Define the timezone
# dublin_tz = pytz.timezone('Europe/Dublin')

# # Current date
# current_date = datetime.now(dublin_tz)

# # Regular expressions
# month_regex = r'(\d+(?:st|nd|rd|th)?)\s*[-_,]?\s*(?:of\s*)?[-_,]?\s*(January|February|March|April|May|June|July|August|September|October|November|December)\s*[-_,]?\s*(\d{4}|\d{2})'
# abbrev_month_regex = r'(\d+(?:st|nd|rd|th)?)\s*[-_,]?\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*[-_,]?\s*(\d{4}|\d{2})'
# date_regex = r'(\d{1,2})[_./](\d{1,2})[_./](\d{2}|\d{4})'

# # Split text into sections
# sections = text.split('-----')
# for section in sections:
#     soup = BeautifulSoup(section, 'html.parser')
#     section_text = soup.select_one('.field__item').get_text()
#     (earliest, last) = analyse_text_for_earliest_and_last_date(section_text)
#     print(f"earliest: {earliest}, last: {last}")
# dates_found = {}

# section_counter = 1

# for section in sections:
#     # Clean up the section
#     section = section.strip()
#     if not section:
#         continue
#     soup = BeautifulSoup(section, 'html.parser')
#     section_text = soup.select_one('.field__item').get_text()
    

#     # Initialize the list for the current section
#     dates_found[section_counter] = []

#     # Match full month names and abbreviations
#     month_matches = re.findall(month_regex, section_text)
#     abbrev_matches = re.findall(abbrev_month_regex, section_text)
    
#     # Combine matches
#     for match in month_matches + abbrev_matches:
#         number_before = match[0]
#         month_name = match[1]
#         number_after = match[2]
#         dates_found[section_counter].append(f"{number_before} {month_name} {number_after}")

#     # Match dd/mm/yy or dd/mm/yyyy dates
#     date_matches = re.findall(date_regex, section)
#     for day, month, year in date_matches:
#         dates_found[section_counter].append(f"{day}/{month}/{year}")

#     # Increment the section counter
#     section_counter += 1

# # Print results
# for section, dates in dates_found.items():
#     #print(f"Section {section}:")
#     converted_dates = [parser.parse(date, fuzzy=True).astimezone(dublin_tz) for date in dates]
#     unique_dates = set(converted_dates)

#     if len(unique_dates) == 1:
#         unique_date = next(iter(unique_dates))  # Get the single unique date
        
#         # Check if the unique date is less than a week after the current date
#         if unique_date < current_date or (current_date <= unique_date < current_date + timedelta(weeks=1)):
#             earliest = unique_date - relativedelta(months=1)
#         else:
#             earliest = dublin_tz.localize(datetime.combine(current_date, datetime.min.time().replace(hour=9)))

    #     latest = unique_date.replace(hour=16, minute=0, second=0, microsecond=0).astimezone(dublin_tz)
    #     print(f"Section {section}: Earliest: {earliest.date()}, Latest: {latest.date()}")
    # elif len(unique_dates) > 1:
    #     # Print the earliest and latest dates
    #     earliest = min(converted_dates).replace(hour=9, minute=0, second=0, microsecond=0).astimezone(dublin_tz)
    #     latest = max(converted_dates).replace(hour=16, minute=0, second=0, microsecond=0).astimezone(dublin_tz)
    #     print(f"Section {section}: Earliest: {earliest.date()}, Latest: {latest.date()}")
    # #for date in dates:
    #     #print(f" - {date}")
    
