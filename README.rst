=======================
Parsing Wikipedia pages
=======================
.. contents:: **Contents**
   :depth: 4
   :local:
   :backlinks: top
   
Extract information from infobox
================================
Extract DOB, birthplace, DOD and deathplace
-------------------------------------------
`:information_source:` The script can be found at `extract_born_and_died_from_infobox.py <./scripts/extract_born_and_died_from_infobox.py>`_

This is the environment on which the script was tested:

* **Platform:** macOS
* **Python**: version **3.7**
* `beautifulsoup4 <https://www.crummy.com/software/BeautifulSoup/>`_: **v4.11.1**, for screen-scraping

This is an output of the script::

   ############################
   Processing page 16: Lev_Landau.html

   DOB extraction from different methods
   1st method: 1908-01-22
   2nd method: None
   3rd method: 1908-01-22
   4th method: 1908-01-22
   5th method: None
   6th method: 22 january 1908
   Birthplace: Baku, Baku Governorate, Russian Empire

   DOD extraction from different methods
   2nd method: None
   3rd method: 1968-04-01
   4th method: 1968-04-01
   5th method: None
   6th method: 1 april 1968
   Deathplace: Moscow, Russian SFSR, Soviet Union
   ############################



   ############################
   Processing page 17: Louis_de_Broglie.html

   DOB extraction from different methods
   1st method: 1892-08-15
   2nd method: None
   3rd method: 1892-08-15
   4th method: 1892-08-15
   5th method: None
   6th method: 15 august 1892
   Birthplace: Dieppe, France

   DOD extraction from different methods
   2nd method: None
   3rd method: 1987-03-19
   4th method: 1987-03-19
   5th method: None
   6th method: 19 march 1987
   Deathplace: Louveciennes, France
   ############################



   ############################
   Processing page 18: Ludwig_Boltzmann.html

   DOB extraction from different methods
   1st method: 1844-02-20
   2nd method: None
   3rd method: 1844-02-20
   4th method: 1844-02-20
   5th method: None
   6th method: 20 february 1844
   Birthplace: Vienna, Austrian Empire

   DOD extraction from different methods
   2nd method: None
   3rd method: 1906-09-05
   4th method: 1906-09-05
   5th method: None
   6th method: 5 september 1906
   Deathplace: Tybein, Triest, Austria-Hungary
   ############################



   ############################
   Processing page 19: Max_Born.html

   DOB extraction from different methods
   1st method: 1882-12-11
   2nd method: None
   3rd method: 1882-12-11
   4th method: 1882-12-11
   5th method: None
   6th method: 11 december 1882
   Birthplace: Breslau, German Empire

   DOD extraction from different methods
   2nd method: None
   3rd method: 1970-01-05
   4th method: 1970-01-05
   5th method: None
   6th method: 5 january 1970
   Deathplace: Göttingen, West Germany
   ############################



   ############################
   Processing page 20: Murray_Gell-Mann.html

   DOB extraction from different methods
   1st method: 1929-09-15
   2nd method: None
   3rd method: 1929-09-15
   4th method: 1929-09-15
   5th method: September 15, 1929
   6th method: None
   Birthplace: Manhattan, New York City, U.S.

   DOD extraction from different methods
   2nd method: None
   3rd method: 2019-05-24
   4th method: 2019-05-24
   5th method: May 24, 2019
   6th method: None
   Deathplace: Santa Fe, New Mexico, U.S.
   ############################



   ############################
   Processing page 21: Paul_Dirac.html

   DOB extraction from different methods
   1st method: 1902-08-08
   2nd method: None
   3rd method: 1902-08-08
   4th method: 1902-08-08
   5th method: None
   6th method: 8 august 1902
   Birthplace: Bristol, England

   DOD extraction from different methods
   2nd method: None
   3rd method: 1984-10-20
   4th method: 1984-10-20
   5th method: None
   6th method: 20 october 1984
   Deathplace: Tallahassee, Florida, U.S.
   ############################

`:star:` In the following, I will be explaining the most important parts of the script.

|

Part 1: Checking if a Wikipedia page has an infobox
"""""""""""""""""""""""""""""""""""""""""""""""""""
.. code-block:: python

   bs = BeautifulSoup(text, 'html.parser')
   b_tag = bs.select('p > b')
   tab_tag = bs.select('.infobox.biography.vcard')

`:information_source:` The infobox table for a given Wikipedia page is found within a ``<table>`` tag w
ith the following classes: ``infobox vcard``. This table contains biographical information about a famous person.

For example: `wikipedia.org/wiki/Edward_Teller <https://en.wikipedia.org/wiki/Edward_Teller>`_

`:warning:` The grand majority of Wikipedia pages analyzed (79%, 497 pages over 641) uses ``<table>`` with three classes: ``infobox biography vcard``. However, there is still a very small minority (1%, 9 pages) who relies on two of the classes:  ``infobox vcard``. Thus, it is better to search for ``<table class="infobox vcard">`` to catch as many Wikipedia pages with an infobox as possible.

|

Part 2: Search for the infobox labels 'Born' and 'Died'
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
Once an infobox was found within a Wikipedia page, we can search for the desired infobox labels, in this case: 'Born' and 'Died'.

.. code-block:: python

    # Found infobox. Now search for the desired infobox labels
    th_tags = tab_tag[0].select('tbody > tr > .infobox-label')
    for th_tag in th_tags:
        infobox_label = th_tag.string
        if infobox_label is None:
            continue
        infobox_label = unicodedata.normalize('NFKD', infobox_label)
        td_tag = th_tag.parent.select('.infobox-data')[0]
        if infobox_label == 'Born':
            # Process content associated with the 'Born' label
        elif infobox_label == 'Died':
            # Process content associated with the 'Died' label

`:information_source:` Explanation of the above Python code used for retrieving infobox labels

1. An infobox label associated with a row in an infobox table is found within the ``<th>`` tag with the ``.infobox-label`` class
   
   Thus the infobox label is found in the following *HTML* structure::
   
    <tbody> <tr> <th class='infobox-label'>Born</th>
 
2. ``th_tags`` is a list containing all the labels of an infobox table which we iterate until we find an infobox label (i.e. it is not ``None``)
3. Cleanup the infobox label a little bit by removing non-breaking spaces (``\xa0``) with Python built-il module 
   `unicodedata.normalize <https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize>`_
   (For more information, check `stackoverflow.com/a/48286252 <https://stackoverflow.com/a/48286252>`_)
4. Get the infobox data associated with the given label by retrieving it from ``<th>``'s parent which is a ``<tr>`` tag. From this ``<tr>`` tag, 
   you can get the infobox data within a ``<td>`` tag
   
   Thus the infobox data is found in the following *HTML* structure::
   
    <tbody> <tr> <td class='infobox-data'>"January 15, 1908"</td>
5. If the infobox label is the correct one ('Born' or 'Died'), then it will be processed accordingly to remove the dates

|

Part 3: Get the DOB and DOD
"""""""""""""""""""""""""""
`:information_source:` Methods 2-6 are implemented within the function `extract_dates(td_tag) <./scripts/extract_born_and_died_from_infobox.py#L34>`_

Method #1: ``.bday`` (simplest)
'''''''''''''''''''''''''''''''
The simplest method for retrieving the DOB in an infobox is to look for it in a ``<span>`` tag with the ``bday`` class, like this 
`HTML code <https://en.wikipedia.org/wiki/Abdus_Salam>`_::

 <td class="infobox-data"><span style="display:none">(<span class="bday">1926-01-29</span>)</span>

|

Python code that searches any tag (``<span>``) with the ``bday`` class starting from ``<td>`` (explained in `section 2 <#part-2-search-for-the-infobox-labels-born-and-died>`_):

.. code-block:: python

    if td_tag.select('.bday'):
       dob = td_tag.select('.bday')[0].string
   else:
       # Use other methods to retrieve the DOB
       dob = None

`:information_source:` If no DOB could be found with this simple method, then other more complex methods involving regex will be deployed as it is
explained in the following sections.

|

Method #2: ``YYYY`` at the beginning, e.g. 1900
'''''''''''''''''''''''''''''''''''''''''''''''
.. code-block:: python

   def extract_dates(td_tag):
       text = clean_data(td_tag.text)
       dates = {'first_date': None, 'second_date': None, 'third_date': None, 'fourth_date': None}
       # Check for different patterns of dates
       # Date pattern #1: YYYY usually at the beginning of the text
       # e.g. 1944 (age 77–78)
       match = re.search(r"^(\d{3,4})", text, re.MULTILINE)
       if match:
           first_date = match.group()
       else:
           first_date = None
       dates['first_date'] = first_date

Method #3: ``YYYY-MM-DD`` with regex, e.g. 1500-01-19
'''''''''''''''''''''''''''''''''''''''''''''''''''''
.. code-block:: python

    # Date pattern #2: YYYY-MM-DD with regex
    match = re.search(r"\d+-\d{1,2}-\d{1,2}", text, re.MULTILINE)
    if match:
        second_date = match.group()
    else:
        second_date = None
    dates['second_date'] = second_date

Method #4: ``YYYY-MM-DD`` without regex, e.g. 1500-01-19
''''''''''''''''''''''''''''''''''''''''''''''''''''''''
.. code-block:: python

    # Date pattern #3: YYYY-MM-DD without regex
    third_date = None
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
                third_date = date
                break
    dates['third_date'] = third_date

Method #5: ``Month Day, Year``, e.g. January 19, 1500
'''''''''''''''''''''''''''''''''''''''''''''''''''''
.. code-block:: python

    # Date pattern #4: Month Day, Year, e.g. January 19, 2019
    regex = r"(?P<month>january|february|march|april|may|june|july|august|september|october|" \
            r"november|december)\s*((?P<day>\d+)),\s*(?P<year>\d+)"
    match = re.search(regex, text.lower(), re.MULTILINE)
    if match:
        fourth_date = match.group().capitalize()
        # Keep only one space between parts of date
        subst = "\\g<month> \\g<day>, \\g<year>"
        fourth_date = re.sub(regex, subst, fourth_date, 0, re.MULTILINE)
    else:
        fourth_date = None
    dates['fourth_date'] = fourth_date

Method #6: ``Day Month Year``, e.g. 19 January 1500
'''''''''''''''''''''''''''''''''''''''''''''''''''
.. code-block:: python

    # Date pattern #5: Day Month Year, e.g. 19 January   2019
    # e.g. Anatoly Aleksandrovich Vlasov20 August  1908Balashov, Russian Empire
    regex = r"(?P<day>\d{1,2})(?P<space1>\s*)(?P<month>[j|J]anuary|[f|F]ebruary|" \
            r"[m|M]arch|[a|A]pril|[m|M]ay|june|[j|J]uly|[a|A]ugust|[s|S]eptember|" \
            r"[o|O]ctober|[n|N]ovember|[d|D]ecember)(?P<space2>\s*)(?P<year>\d+)"
    match = re.search(regex, text.lower(), re.MULTILINE)
    if match:
        fifth_date = match.group()
        # Keep only one space between parts of date
        subst = "\\g<day> \\g<month> \\g<year>"
        fifth_date = re.sub(regex, subst, fifth_date, 0, re.MULTILINE)
    else:
        fifth_date = None
    dates['fifth_date'] = fifth_date

Part 4: Get the birth and death places
""""""""""""""""""""""""""""""""""""""
`:information_source:` The extraction of the birth and death places are done within the function `extract_place(td_tag, kind_place='birthplace') <./scripts/extract_born_and_died_from_infobox.py#L15>`_

|

.. code-block:: python

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

