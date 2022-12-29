=======================
Parsing Wikipedia pages
=======================
.. contents:: **Contents**
   :depth: 4
   :local:
   :backlinks: top
   
Extract information from infobox
================================
Many Wikipedia pages have an infobox table with important information about the subject of the page. Thus for a famous person, we
can expect for this table to have the following information: DOB, DOD, Alma mater, Education, Known for, Awards, ...

Extract DOB, birthplace, DOD and deathplace
-------------------------------------------
`:information_source:` 
 
 - DOB: Day Of Birth
 - DOD: Day of Death
 - The script can be found at `extract_born_and_died_from_infobox.py <./scripts/extract_born_and_died_from_infobox.py>`_.

This is the environment on which the script was tested:

* **Platform:** macOS
* **Python**: version **3.7**
* `beautifulsoup4 <https://www.crummy.com/software/BeautifulSoup/>`_: **v4.11.1**, for screen-scraping

`:warning:` In order to run the script, you need first to have a folder with all the Wikipedia pages (\*.html) you want to parse. Then, you need
to give the path to this folder to the script, like this::

 $ python extract_from_infobox.py ~/Data/wikipedia/physicists

Sample output of the script::

   ############################
   Processing page 16: Lev_Landau.html

   DOB extraction from different methods
   1st method: 1908-01-22
   2nd method: None
   3rd method: 1908-01-22
   4th method: 1908-01-22
   5th method: None
   6th method: 22 January 1908
   Birthplace: Baku, Baku Governorate, Russian Empire

   DOD extraction from different methods
   2nd method: None
   3rd method: 1968-04-01
   4th method: 1968-04-01
   5th method: None
   6th method: 1 April 1968
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
   6th method: 15 August 1892
   Birthplace: Dieppe, France

   DOD extraction from different methods
   2nd method: None
   3rd method: 1987-03-19
   4th method: 1987-03-19
   5th method: None
   6th method: 19 March 1987
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
   6th method: 20 February 1844
   Birthplace: Vienna, Austrian Empire

   DOD extraction from different methods
   2nd method: None
   3rd method: 1906-09-05
   4th method: 1906-09-05
   5th method: None
   6th method: 5 September 1906
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
   6th method: 11 December 1882
   Birthplace: Breslau, German Empire

   DOD extraction from different methods
   2nd method: None
   3rd method: 1970-01-05
   4th method: 1970-01-05
   5th method: None
   6th method: 5 January 1970
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
   6th method: 8 August 1902
   Birthplace: Bristol, England

   DOD extraction from different methods
   2nd method: None
   3rd method: 1984-10-20
   4th method: 1984-10-20
   5th method: None
   6th method: 20 October 1984
   Deathplace: Tallahassee, Florida, U.S.
   ############################

`:information_source:`

 - The methods used for extracting the DOB and DOD are explained in `Part 3 <#part-3-get-the-dob-and-dod>`_.
 - All methods 2-6 are used for extracting both the DOB and DOD. However, `method 1 <#method-1-bday-simplest>`_ is only used
   for extracting the DOB.
 - The same method is used for extracting the birthplace and deathplace, as explained in `Part 4 <#part-4-get-the-birth-and-death-places>`_.

`:star:` In the following, I will be explaining the most important parts of the script.

|

Part 1: Checking if a Wikipedia page has an infobox
"""""""""""""""""""""""""""""""""""""""""""""""""""
.. code-block:: python

   bs = BeautifulSoup(text, 'html.parser')
   b_tag = bs.select('p > b')
   tab_tag = bs.select('.infobox.biography.vcard')

`:information_source:` The infobox table for a given Wikipedia page is found within a ``<table>`` tag with the following classes: ``infobox vcard``. This table contains biographical information about a famous person.

For example: `wikipedia.org/wiki/Edward_Teller <https://en.wikipedia.org/wiki/Edward_Teller>`_

`:warning:` The grand majority of Wikipedia pages analyzed (79%, 497 pages over 641) uses ``<table>`` with three classes: ``infobox biography vcard``. However, there is still a very small minority (1%, 9 pages) who relies on two of the classes:  ``infobox vcard``. Thus, it is better to search for ``<table class="infobox vcard">`` to catch as many Wikipedia pages with an infobox as possible.

|

Part 2: Search for the infobox labels 'Born' and 'Died'
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
Once an infobox is found within a Wikipedia page, we can search for the desired infobox labels, in this case: 'Born' and 'Died'.

.. code-block:: python

    # Found infobox. Now search for the desired infobox labels
    th_tags = tab_tag[0].select('tbody > tr > .infobox-label')
    for th_tag in th_tags:
        infobox_label = th_tag.string
        if infobox_label is None:
            continue
        infobox_label = unicodedata.normalize('NFC', infobox_label)
        td_tag = th_tag.parent.select('.infobox-data')[0]
        if infobox_label == 'Born':
            # Process content associated with the 'Born' label
        elif infobox_label == 'Died':
            # Process content associated with the 'Died' label

`:information_source:` Explanation of the above Python code used for retrieving infobox labels

1. An infobox label associated with a row in an infobox table is found within the ``<th>`` tag with the ``.infobox-label`` class
   
   Thus the infobox label 'Born' is found in the following *HTML* structure::
   
    <tbody> <tr> <th class='infobox-label'>Born</th>
 
2. ``th_tags`` is a list containing all the labels of an infobox table which we iterate until we find an infobox label (i.e. it is not ``None``).
3. Cleanup the infobox label a little bit by removing non-breaking spaces (``\xa0``) with Python built-in module 
   `unicodedata.normalize <https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize>`_
   (For more information, check `stackoverflow.com/a/48286252 <https://stackoverflow.com/a/48286252>`_).
4. Get the infobox data associated with the given label by retrieving it from ``<th>``'s parent which is a ``<tr>`` tag. From this ``<tr>`` tag, 
   you can get the infobox data within a ``<td>`` tag. The infobox data contains the useful information we are looking to extract
   for a given label, e.g. the DOB and birthplace.
   
   Thus the infobox data for a 'Born' label is found in the following *HTML* structure::
   
    <tbody> <tr> <td class='infobox-data'>"January 15, 1908"</td>
5. If the infobox label is the correct one ('Born' or 'Died'), then it will be processed accordingly to remove the dates.

|

Part 3: Get the DOB and DOD
"""""""""""""""""""""""""""
`:information_source:` Methods 2-6 are implemented within the function `extract_dates(td_tag) <./scripts/extract_born_and_died_from_infobox.py#L35>`_.

Method #1: ``.bday`` (simplest)
'''''''''''''''''''''''''''''''
The simplest method for retrieving the DOB in an infobox is to look for it in a ``<span>`` tag with the ``bday`` class, like in this 
`HTML code <https://en.wikipedia.org/wiki/Abdus_Salam>`_::

 <td class="infobox-data"><span style="display:none">(<span class="bday">1926-01-29</span>)</span>

|

Python code that searches any tag (``<span>``) with the ``bday`` class starting from ``<td>`` (explained in `Part 2 <#part-2-search-for-the-infobox-labels-born-and-died>`_):

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

`:information_source:` 

 - The second method searches the text from the given ``<td>`` tag for any pattern of number with 3 or 4 digits at the 
   beginning of the text, e.g. 1944 (age 77–78).
 - The reason for specifying the number of digits in the regex is that if we don't then we might also catch numbers that 
   correspond to the day of the DOB/DOD, e.g. 20 October 1984.

|

Method #3: ``YYYY-MM-DD`` with regex only, e.g. 1500-01-19
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
.. code-block:: python

    # Date pattern #2: YYYY-MM-DD with regex
    match = re.search(r"\d+-\d{1,2}-\d{1,2}", text, re.MULTILINE)
    if match:
        second_date = match.group()
    else:
        second_date = None
    dates['second_date'] = second_date

`:information_source:` 

 - The third method searches the text from the given ``<td>`` tag for any pattern of numbers respecting the
   format ``YYYY-MM-DD`` with the year part starting at year 1 and for the other parts (month and day) having one or two digits.
 - Dates that should be matched: ``15-1-2`` and ``1987-08-12``.
 - Dates that should not be matched: ``1947-123-2`` and ``-11-10``.

|

Method #4: ``YYYY-MM-DD`` with ``<span>``, e.g. 1500-01-19
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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

`:information_source:` 

 1. The fourth method selects all the ``<span>`` tags starting from the given ``<td>`` tag. The first of these ``<span>`` tag that
    has the ``style='display:none'`` attribute gets analyzed further.
 2. The text found within this ``<span>`` tag gets cleaned up (removing any citation number/text within square brackets and so on, see
    the `clean_data(data) <#scripts/extract_born_and_died_from_infobox.py#L11>`_ function) and its parentheses are removed. 
    
    Example: '(2001-01-15)' --> '2001-01-15'
 3. Finally, just to make sure that the found date is in the correct format (YYYY-MM-DD), it is analyzed with a regex and if it is found
    to be a valid date then it is retained.
|

Method #5: ``Month Day, Year``, e.g. January 19, 1500
'''''''''''''''''''''''''''''''''''''''''''''''''''''
.. code-block:: python

    # Date pattern #4: Month Day, Year, e.g. January 19, 2019
    regex = r"(?P<month>january|february|march|april|may|june|july|august|september|october|" \
            r"november|december)\s*((?P<day>\d+)),\s*(?P<year>\d+)"
    match = re.search(regex, text.lower(), re.MULTILINE)
    if match:
        day = match.groupdict()['day']
        month = match.groupdict()['month'].capitalize()
        year = match.groupdict()['year']
        fourth_date = f'{month} {day}, {year}'
    else:
        fourth_date = None
    dates['fourth_date'] = fourth_date

|

`:information_source:` 

 - The fifth method searches the text from the given ``<td>`` tag for any pattern of text respecting the
   format ``Month Day, Year``.
 - The text searched by the regex is first put all in lowercase so we can take into account cases where the dates 
   were entered with any of letters of the month capitalized, e.g. JAnuary 19, 2019 or apriL 15, 1994.
 - Named groups are used when building the long regex so it is easier to reconstruct the date afterward with the correct format, especially if the
   initial date had more than one space between its different parts, e.g. ``January 19,     2019``.

|

Method #6: ``Day Month Year``, e.g. 19 January 1500
'''''''''''''''''''''''''''''''''''''''''''''''''''
.. code-block:: python

    # Date pattern #5: Day Month Year, e.g. 19 January   2019
    # e.g. Anatoly Aleksandrovich Vlasov20 August  1908Balashov, Russian Empire
    regex = r"(?P<day>\d{1,2})(?P<space1>\s*)(?P<month>january|february|march|april|may|june|" \
            r"july|august|september|october|november|december)(?P<space2>\s*)(?P<year>\d+)"
    match = re.search(regex, text.lower(), re.MULTILINE)
    if match:
        day = match.groupdict()['day']
        month = match.groupdict()['month'].capitalize()
        year = match.groupdict()['year']
        fifth_date = f'{day} {month} {year}'
    else:
        fifth_date = None
    dates['fifth_date'] = fifth_date

`:information_source:` 

 - The sixth method searches the text from the given ``<td>`` tag for any pattern of text respecting the
   format ``Day Month Year``.
 - The same explanations for the `fifth method <#method-5-month-day-year-e-g-january-19-1500>`_ applies here so we won't repeat them.

|

Part 4: Get the birth and death places
""""""""""""""""""""""""""""""""""""""
`:information_source:` The extraction of the birth and death places are done within the function `extract_place(td_tag, kind_place='birthplace') <./scripts/extract_born_and_died_from_infobox.py#L15>`_

|

Since the code for the ``extract_place()`` function is simple, all three methods will be explained here instead of doing it separately like it was donne for the DOB/DOD extraction methods from `Part 3 <#part-3-get-the-dob-and-dod>`_. 

.. code-block:: python

   def extract_place(td_tag, kind_place='birthplace'):
       assert kind_place in ['birthplace', 'deathplace']
       text = td_tag.text
       # Method 1
       if td_tag.select(f'.{kind_place}'):
           place = clean_data(td_tag.select(f'.{kind_place}')[0].text)
       else:
           # Method 2
           if 'aged' in text:
               # e.g. February 8, 1957(1957-02-08) (aged 53)Washington, D.C., U.S.
               match = re.search(r"aged\s*\d+\)(.*)$", text, re.MULTILINE)
           else:
               # Method 3
               # Get the birthplace/deathplace after the DOB/DOD year
               # e.g. Neumann János Lajos(1903-12-28)December 28, 1903Budapest, Kingdom of Hungary, Austria-Hungary
               match = re.search(r",\s*\d+(.*)$", text, re.MULTILINE)
           if match:
               place = match.groups()[0]
           else:
               place = None
       return place

`:information_source:`

 1. The ``kind_place`` parameter takes two values: 'birthplace' or 'deathplace'.
 2. The **first method** used to retrieve the birthplace/deathplace searches for any tag (``<div>``) with the 
    ``birthplace|deathplace`` class. The text for this ``<div>`` tag is the place we are looking for.
    
    The 'birthplace' or 'deathplace' is found in the following *HTML* structure::
    
     <div style="display:inline" class="birthplace">Moscow, Russia</div>
 3. The **second method** only applies to the extraction of the deathplace. It searches the text from the ``<td>`` tag 
    (see `Part 2 <#part-2-search-for-the-infobox-labels-born-and-died>`_) for any string that follows the word 'aged' plus any number
    of spaces and a closed parenthesis, e.g. ``aged 53)Washington, D.C., U.S.`` This string should be the deathplace we are searching for.
 4. The **third method** retrieves the birthplace/deathplace by searching the same text like in the secod method but looks for any
    string that follows a comma followed by any number of spaces and the year, e.g. ``28, 1903Budapest, Kingdom of Hungary, 
    Austria-Hungary``. This string should be the birthplace/deathplace we are looking for.
