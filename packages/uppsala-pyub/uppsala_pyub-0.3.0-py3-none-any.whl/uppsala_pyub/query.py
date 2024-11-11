#!/usr/bin/env python3
"""
Query the Uppsala University Library search service
"""
from uppsala_pyub.soup import make_soup
import re




def query_template():
    """
    Return a dictionary of query key-value pairs and default values.
    """
    return {
        "output_destination": "./",
        "creator": None,
        "creator_precision": "contains",
        "title": None,
        "title_precision": "contains",
        "creation_from": None,
        "creation_to": None,
        "resource_type": None,
        "join_by": "AND",
        "query": None,
        "language": "en",
    }


def cap_query(query):
    """
    fill in all the missing variable to make a complete query dict
    """
    t = query_template()
    for k, v in t.items():
        if k not in query:
            query[k] = v
    return query


def format_date_string(datestring, startdate=True):
    """
    Format the datestring to YYYY-mm-dd format.

    Startdate provede 01-01 to a year, else 12-31

    This function assumes input is in YYYY format. Fully formed dates are returned as is, and in YYYY-mm, the month will be overwritten according to the startdate parameter.
    """
    pat = re.compile(r'\d{4}-\d{2}-\d{2}')
    if pat.search(datestring) is not None:
        return datestring
    try:
        _ = int(datestring[:4])
        if startdate:
            formatted_datestring = f"{datestring[:4]}-01-01"
        else:
            formatted_datestring = f"{datestring[:4]}-12-31"
        return formatted_datestring
    except:
        ValueError(f"Bad datestring: I don't know how to format your datestring entry {datestring}.")


def format_creator_names(names):
    """
    returns a list of creators, e.g. when passed a multi author citation `Smith and Doe`
    """
    formatted_names = []
    pat = re.compile(r'(,|and|&)')
    names = pat.sub("|", names)
    formatted_names.extend([_.strip() for _ in names.split("|") if _.strip() != ''])
    return formatted_names


def search_url(**kwargs):
    """
    Construct search URL based on kwarg parameters.
    """
    base_url = "https://uub.primo.exlibrisgroup.com/discovery/search?"
    tabscope = f"tab=Everything&search_scope=MyInst_and_CI&vid=46LIBRIS_UUB:UUB&lang={kwargs.get("language")}&mode=advanced&offset=0"
    filters = []

    if kwargs.get("query") is None:
        queries = []
        if kwargs.get("creator") is not None:
            creators = format_creator_names(kwargs.get("creator"))
            for c in creators:
                queries.append("query=creator," + kwargs.get('creator_precision') + "," + c)
        if kwargs.get("title") is not None:
            queries.append("query=title," + kwargs.get("title_precision") + "," + kwargs.get("title"))
        query = f",{kwargs.get('join_by')}&".join(queries)
    else:
        query = kwargs.get("query")
    if kwargs.get("resource_type") is not None:
        filters.append("pfilter=rtype,exact," + kwargs.get("resource_type"))
    if kwargs.get("creation_from") is not None:
        filters.append(f"pfilter=dr_s,exact,{format_date_string(kwargs.get('creation_from'))}")
        if kwargs.get("creation_to") is None:
            filters.append(f"pfilter=dr_e,exact,{format_date_string(kwargs.get('creation_from'), startdate=False)}")
        else:
            filters.append(f"pfilter=dr_e,exact,{format_date_string(kwargs.get('creation_to'), startdate=False)}")
    url = base_url + query
    if filters is not None and len(filters) > 0:
        url = url + ",AND&" + ",AND&".join(filters)
    url = url + ",AND&" + tabscope
    return url


def run_search(**kwargs):
    """
    Run a search based on key-word arguments. See ./cli.py for a list of accepted keywords.

    Returns:
        soup: (bs4 object) parsed result of the url
        url (str): UU UB search url
    """
    url = search_url(**kwargs)
    print("\n\n", url, "\n\n")
    soup = make_soup(url)
    return soup, url

