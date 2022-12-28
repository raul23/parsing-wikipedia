import os
import re
import unicodedata
from pathlib import Path

from bs4 import BeautifulSoup

# import ipdb


def clean_data(data):
    return unicodedata.normalize('NFC', re.sub(r"\[.+\]", '', data, 0, re.MULTILINE).replace('\xa0', ' '))


def extract_place(td_tag, kind_place='birthplace'):
    text = td_tag.text
    if td_tag.select(f'.{kind_place}'):
        place = clean_data(td_tag.select(f'.{kind_place}')[0].text)
    else:
        if 'aged' in text:
            # e.g. February 8, 1957(1957-02-08) (aged 53)Washington, D.C., U.S.
            match = re.search(r"aged\s*\d+\)(.*)$", text, re.MULTILINE)
        else:
            # Get the birthplace/deathplace after the DOB/DOD year
            # e.g. Neumann János Lajos(1903-12-28)December 28, 1903Budapest, Kingdom of Hungary, Austria-Hungary
            match = re.search(r",\s*\d+(.*)$", text, re.MULTILINE)
        if match:
            place = match.groups()[0]
        else:
            place = None
    return place


def extract_dates(td_tag):
    text = td_tag.text
    dates = {'first_date': None, 'second_date': None, 'third_date': None, 'fourth_date': None}
    # Check for different patterns of dates
    # Date pattern #1: YYYY-MM-DD with regex
    match = re.search(r"\d+-\d{1,2}-\d{1,2}", text, re.MULTILINE)
    if match:
        first_date = match.group()
    else:
        first_date = None
    dates['first_date'] = first_date

    # Date pattern #2: YYYY-MM-DD without regex
    second_date = None
    span_tags = td_tag.select('span')
    for span_tag in span_tags:
        if span_tag.get('style') == 'display:none':
            date = clean_data(span_tag.text)
            # Remove parentheses from date
            # e.g. '(2001-01-15)' --> '2001-01-15'
            date = date.replace('(', '').replace(')', '')
            # Check it is in the correct format
            match = re.search(r"\d+-\d{1,2}-\d{1,2}", date, re.MULTILINE)
            if match:
                second_date = date
                break
    dates['second_date'] = second_date

    # Date pattern #3: Month Day, Year, e.g. January 19, 2019
    regex = r"(?P<month>january|february|march|april|may|june|july|august|september|october|" \
            r"november|december)\s*((?P<day>\d+)),\s*(?P<year>\d+)"
    match = re.search(regex, text.lower(), re.MULTILINE)
    if match:
        third_date = match.group().capitalize()
        # Keep only one space between parts of date
        subst = "\\g<month> \\g<day>, \\g<year>"
        third_date = re.sub(regex, subst, third_date, 0, re.MULTILINE)
    else:
        third_date = None
    dates['third_date'] = third_date

    # Date pattern #4: Day Month Year, e.g. 19 January   2019
    # e.g. Anatoly Aleksandrovich Vlasov20 August  1908Balashov, Russian Empire
    regex = r"(?P<day>\d{1,2})(?P<space1>\s*)(?P<month>[j|J]anuary|[f|F]ebruary|" \
            r"[m|M]arch|[a|A]pril|[m|M]ay|june|[j|J]uly|[a|A]ugust|[s|S]eptember|" \
            r"[o|O]ctober|[n|N]ovember|[d|D]ecember)(?P<space2>\s*)(?P<year>\d+)"
    match = re.search(regex, text.lower(), re.MULTILINE)
    if match:
        fourth_date = match.group()
        # Keep only one space between parts of date
        subst = "\\g<day> \\g<month> \\g<year>"
        fourth_date = re.sub(regex, subst, fourth_date, 0, re.MULTILINE)
    else:
        fourth_date = None
    dates['fourth_date'] = fourth_date

    print(f'First date: {first_date}')
    print(f'Second date: {second_date}')
    print(f'Third date: {third_date}')
    print(f'Fourth date: {fourth_date}')
    return dates


number_infobox = 0
input_directory = Path(os.path.expanduser('~/Data/wikipedia/physicists'))
for i, filepath in enumerate(input_directory.rglob('*.html'), start=1):
    print('############################')
    print(f'Process page {i}: {filepath}')
    with open(filepath, 'r') as f:
        text = f.read()
    bs = BeautifulSoup(text, 'html.parser')
    b_tag = bs.select('p > b')
    tab_tag = bs.select('.infobox.vcard')
    if tab_tag:
        # Found infobox
        number_infobox += 1
        th_tags = tab_tag[0].select('tbody > tr > .infobox-label')
        for th_tag in th_tags:
            infobox_label = th_tag.string
            if infobox_label is None:
                continue
            # Clean infobox label by replacing \xa0 with ' '
            # \xa0 is actually non-breaking space in Latin1 (ISO 8859-1), also chr(160)
            # Ref.: https://stackoverflow.com/a/11566398
            infobox_label = unicodedata.normalize('NFKD', infobox_label)
            # From the <tr> tag, get the infobox-data containing the relevant Born or Died information
            td_tag = th_tag.parent.select('.infobox-data')[0]
            td_tag_text = clean_data(td_tag.text)
            if infobox_label == 'Born':
                if td_tag.select('.bday'):
                    dob = td_tag.select('.bday')[0].string
                else:
                    dob = None
                    extract_dates(td_tag)
                birthplace = extract_place(td_tag)
                print(f'DOB: {dob}')
                print(f'Birthplace: {birthplace}\n')
            elif infobox_label == 'Died':
                extract_dates(td_tag)
                deathplace = extract_place(td_tag, 'deathplace')
                print(f'Deathplace: {deathplace}')
    print('############################\n\n\n')

# ipdb.set_trace()

# 497 infoboxes over 641 wikipedia pages (78%) when using infobox.biography.vcard
# 506 infoboxes over 641 wikipedia pages (79%) when using infobox..vcard
