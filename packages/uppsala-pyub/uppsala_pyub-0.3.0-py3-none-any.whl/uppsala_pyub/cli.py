#!/usr/bin/env python3
"""
Main entrypoint for Uppsala pyub --

Query Uppsala University's holdings via cli or script.

The program runs a qeury, displays results to the user and performs an action on the selected result.
"""
import argparse
from uppsala_pyub.bibtex import make_bibtex
from uppsala_pyub.query import run_search
from uppsala_pyub.handle_results import display_results




def links(xml_data, output_location='.'):
    """
    place holder for eventual action... will probably be additional submodule.
    """
    raise NotImplementedError("`list_links` is not yet implemented.")

def citation(xml_data, output_location='.'):
    """
    place holder for eventual action... will probably be additional submodule.
    """
    raise NotImplementedError("`generate_citation` is not implemented. Fetch bibtex instead.")

def location(xml_data, output_location='.'):
    """
    place holder for eventual action... will probably be additional submodule.
    """
    raise NotImplementedError("`show_physical_location` is not yet implemented.")



#if __name__ == '__main__':
def cli():
    """
    Run command line interface
    """
    citation_formats = {
        "apa-6": "APA (6th edition)",
        "apa-7": "APA (7th edition)",
        "chicago": "Chicago/Turabian (16th edition)",
        "harvard": "Harvard",
        # add rest of styles
    }
    precisions = {
        "contains": "term is contained in the target material",
        "exact": "term is an exact match to target material",
        "begins_with": "target material begins with term",
    }
    resource_types = [
        "books",
        "articles",
        "book_chapter",
    ]

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(help="Chose an action", dest="action")

    # actions:
    ## Fetch a bibtex entru
    fetch_bibtex_parser = subparsers.add_parser("fetch_bibtex", aliases=["bib"], help="Download bibtex entry for the selected resource.")

    ## list links
    list_links_parser = subparsers.add_parser("list_links", aliases=["link"], help="List links to / about the selected resource.")

    ## Generate a citation string
    generate_citation_parser = subparsers.add_parser("generate_citation", aliases=["cit"], help="Generate a citation for the selected resource.")

    generate_citation_parser.add_argument("--format", type=str, choices=list(citation_formats.keys()), default="harvard", help=f"Desited format of the citation string. {citation_formats}")

    ## show locations
    show_location_parser = subparsers.add_parser("show_physical_locations", aliases=["loc"], help="Show physical locations for the selected resource.")

    # shared args
    parser.add_argument("-o", "--output-destination",
                        type=str,
                        default="./",
                        help="Where to write output (if you want to write output). Q")
    parser.add_argument("-c", "--creator",
                        type=str,
                        default=None,
                        help="Creator / Author string. Q")
    parser.add_argument("--creator-precision",
                        type=str,
                        default="contains",
                        choices=list(precisions.keys()),
                        help=f"How do you want to apply the search? {precisions} Q")
    parser.add_argument("-t", "--title",
                        type=str,
                        default=None,
                        help="Title of work. Q")
    parser.add_argument("--title-precision",
                        type=str,
                        default="contains",
                        choices=list(precisions.keys()),
                        help=f"How do you want to apply the search? {precisions} Q")
    parser.add_argument("-s", "--creation_from",
                        type=str,
                        default=None,
                        help="Creation date range start -- YYYY or YYYY-mm-dd -- F")
    parser.add_argument("-e", "--creation_to",
                        type=str,
                        default=None,
                        help="Creation date range end -- YYYY or YYYY-mm-dd -- F")
    parser.add_argument("-T", "--resource-type",
                        type=str,
                        default=None,
                        choices=resource_types,
                        help=f"Select a specific type of resource to find. {resource_types} F")
    parser.add_argument("--join-by",
                        type=str,
                        default="AND",
                        choices=["AND", "OR"],
                        help=f"How to join the query parameters. [\"AND\", \"OR\"]")
    parser.add_argument("-q", "--query",
                        type=str,
                        default=None,
                        help="Enter a custom query")
    parser.add_argument("-l", "--language",
                        type=str,
                        default="en",
                        choices=["en","sv"],
                        help="Language of search interface. [\"en\", \"sv\"]")
    args = parser.parse_args()

    #main program
    programs = {
        "fetch_bibtex": make_bibtex,
        "bib": make_bibtex,
        "list_links": links,
        "generate_citation": citation,
        "show_physical_locations": location,
    }
    result_soup, url = run_search(**vars(args))
    selected = display_results(result_soup, url)
    if selected is not None:
        programs[args.action](selected, output_location=args.output_destination)

