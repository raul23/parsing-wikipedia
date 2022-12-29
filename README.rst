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
Method #1: ``.bday`` (simplest)
'''''''''''''''''''''''''''''''
The simplest method for retrieving the DOB in an infobox is to look for it in a ``<span>`` tag with the ``bday`` class, like this 
`HTML code <https://en.wikipedia.org/wiki/Abdus_Salam>`_::

 <td class="infobox-data"><span style="display:none">(<span class="bday">1926-01-29</span>)</span>

|

Python code that search any tag (``<span>``) with the ``bday`` class starting from ``<td>`` (explained in `section 2 <#part-2-search-for-the-infobox-labels-born-and-died>`_):

.. code-block:: python

    if td_tag.select('.bday'):
       dob = td_tag.select('.bday')[0].string
   else:
       # Use other methods to retrieve the DOB
       dob = None

`:information_source:` If no DOB could be found with this simple method, then other more complex methods involving regex will be deployed as it is
explained in the following sections.

Method #2: ``YYYY-MM-DD`` with regex, e.g. 1500-01-19
'''''''''''''''''''''''''''''''''''''''''''''''''''''
Method #3: ``YYYY-MM-DD`` without regex, e.g. 1500-01-19
''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Method #4: ``Month Day, Year``, e.g. January 19, 1500
'''''''''''''''''''''''''''''''''''''''''''''''''''''
Method #5: ``Day Month Year``, e.g. 19 January 1500
'''''''''''''''''''''''''''''''''''''''''''''''''''

Part 4: Get the birth place
"""""""""""""""""""""""""""

Part 5: Get the death place
"""""""""""""""""""""""""""
