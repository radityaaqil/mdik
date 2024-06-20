from datetime import datetime  
import random
import calendar
import re

#  Parse Date
def parseDate(date_str):
    if date_str == "":
        return ""
    # Extract the date part
    date_part = date_str.split('(')[0].strip()

    # Try parsing with day
    try:
        date_obj = datetime.strptime(date_part, "%B %d, %Y")
    except ValueError:
        # Try parsing without day
        try:
            date_obj = datetime.strptime(date_part, "%B %Y")
            # Generate a random day if day is not present
            year = date_obj.year
            month = date_obj.month
            _, last_day = calendar.monthrange(year, month)
            day = random.randint(1, last_day)
            date_obj = datetime(year, month, day)
        except ValueError:
            # Try parsing with only year
            try:
                date_obj = datetime.strptime(date_part, "%Y")
                # Generate a random month and day if only year is present
                year = date_obj.year
                month = random.randint(1, 12)
                _, last_day = calendar.monthrange(year, month)
                day = random.randint(1, last_day)
                date_obj = datetime(year, month, day)
            except ValueError:
                raise ValueError(f"Cannot parse date: {date_str}")

    return date_obj.strftime("%Y-%m-%d")

# Function to extract award data
def extract_awards(data, title):
    # Regular expressions to extract different types of awards
    win_pattern = re.compile(r'(\d+) wins?')
    nomination_pattern = re.compile(r'(\d+) nominations?')
    oscar_win_pattern = re.compile(r'Won (\d+) Oscars?')
    oscar_nom_pattern = re.compile(r'Nominated for (\d+) Oscars?')
    bafta_win_pattern = re.compile(r'Won (\d+) BAFTA Film Awards?')
    bafta_nom_pattern = re.compile(r'Nominated for (\d+) BAFTA Film Awards?')
    globe_nom_pattern = re.compile(r'Nominated for (\d+) Golden Globes?')
    globe_win_pattern = re.compile(r'Won (\d+) Golden Globes?')
   
    award_info = {
        'title': title,
        'festival_winner': 0,
        'festival_nomination': 0,
        'oscar_winner': 0,
        'oscar_nomination': 0,
        'bafta_winner': 0,
        'bafta_nomination': 0,
        'golden_globe_nomination': 0,
        'golden_globe_winner': 0,
    }

    wins = win_pattern.findall(data)
    if wins:
        award_info['festival_winner'] = int(wins[0])

    nominations = nomination_pattern.findall(data)
    if nominations:
        award_info['festival_nomination'] = int(nominations[0])

    oscars_won = oscar_win_pattern.findall(data)
    if oscars_won:
        award_info['oscar_winner'] = int(oscars_won[0])

    oscars_nominated = oscar_nom_pattern.findall(data)
    if oscars_nominated:
        award_info['oscar_nomination'] = int(oscars_nominated[0])

    bafta_won = bafta_win_pattern.findall(data)
    if bafta_won:
        award_info['bafta_winner'] = int(bafta_won[0])

    bafta_nominated = bafta_nom_pattern.findall(data)
    if bafta_nominated:
        award_info['bafta_nomination'] = int(bafta_nominated[0])

    globes_nominated = globe_nom_pattern.findall(data)
    if globes_nominated:
        award_info['golden_globe_nomination'] = int(globes_nominated[0])

    globe_won = globe_win_pattern.findall(data)
    if globe_won:
        award_info['golden_globe_winner'] = int(globe_won[0])

    return award_info

def awards(data):
    awards_data = []
    #  Extract and categorize awards from each string
    for award_str in data:
        award = award_str['awards']
        title = award_str['title']
        awards_data.append(extract_awards(award, title))
        
    return awards_data


# Parse release date
def parse_released_date(released_str, base_year):
    date_obj = datetime.strptime(released_str, '%d-%b-%y')
    # Ensure the year is correct (handling century if needed)
    if date_obj.year > datetime.now().year:
        date_obj = date_obj.replace(year=date_obj.year - 100)
    return date_obj.strftime('%Y-%m-%d')