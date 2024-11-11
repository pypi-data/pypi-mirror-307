from lxml import etree
from uppsala_pyub.soup import make_soup
import re
import requests
print(etree.__file__)



def fetch_namespace():
    """
    return namespace dict for working with metadata xml
    """
    return {
            "xml":"{http://www.exlibrisgroup.com/xsd/primo/primo_nm_bib}",
            "sear": "{http://www.exlibrisgroup.com/xsd/jaguar/search}"
        }


def get_yatt(root, ns):
    """
    Returns year, author list, title, and resource type.

    Args:
        root: elementtree object -- parsed entry data
        ns: namespace dict
    """
    y, a, t, T = None, None, None, ''
    try:
        y = root.find(f"{ns['xml']}addata/{ns['xml']}date").text
    except:
        y = ""
    try:
        a = [_.text.strip() for _ in root.findall(f"{ns['xml']}addata/{ns['xml']}au") if _.text.strip() != '']
        assert a is not None
        assert len(a) != 0
    except:
        a = [_.text for _ in root.findall(f"{ns['xml']}addata/{ns['xml']}addau")]

    t = root.find(f"{ns['xml']}display/{ns['xml']}title").text
    try:
        T = root.find(f"{ns['xml']}display/{ns['xml']}rtype").text
    except:
        try:
            T = root.find(f"{ns['xml']}display/{ns['xml']}type").text
        except: pass
    return y, a, t, T


def display_results(soup, url):
    """
    Displays the results of a query to the user.

    Args:
        soup: bs4 object -- parsed xml result of query
        url (str): url with search parameters

    Returns:
        selection: etree object -- parsed metadata about selected entry
    """
    def _offset_url(url, value=10, operation="add"):
        def _add(mo, value=value):
            return f"offset={int(mo.group(1))+value}"

        def _subtract(mo, value=value):
            n = int(mo.group(1))-value
            if n < 0:
                n = 0
            return f"offset={n}"

        if operation == "add":
            url = re.sub(r'offset=(\d{1,5})', _add, url)
        elif operation == "subtract":
            url = re.sub(r'offset=(\d{1,5})', _subtract, url)
        else:
            raise ValueError(f"{operation} is not a valid operation. Choose add or subtract.")
        return url

    def _select(D):
        print("\nIs one of these what you're looking for? Select an entry by entering the value from the `Nr` column. or...")
        print("  - Enter `n` to see the next batch of results.")
        if "1" not in D:
            print("  - Enter `p` to see the previous batch of results.")
        print("  - Enter `a` to abort / skip this search attempt.")
        print("  - Enter `r` to reload this batch.")
        in_ = input("Your input: ")
        if in_ in D:
            return D[in_], None
        elif in_ in ["n", "p", "a", "r"]:
            return None, in_
        else:
            print("Invalid entry. Try again!")
            return _select(D)

    def _parse_datafile(data_url):
        data_url = data_url.replace("&amp;", "&")
        #print("~~", data_url)
        response = requests.get(data_url)
        root = etree.fromstring(response.content)
        return root, fetch_namespace()

    def _show(soup):
        items = soup.find_all("prm-brief-result-container")
        D = {}
        print("{:5}| {:12}| {:12}| {:60}| {:70}".format("Nr", "type", "year", "authors", "title"))
        for item in items:
            nr = item.find("span", class_="list-item-count").getText()
            root, ns = _parse_datafile(item.find("span", {"data-url": True}).attrs.get("data-url"))
            D[nr] = root
            year, authors, title, type_ = get_yatt(root, ns)
            print(f"{nr:5}| {type_[:10]:12}| {year[:10]:12}| {'; '.join(authors)[:58]:60}| {title[:68]:70}")
        return D


    selection = None
    action = None
    while selection == None:
        if action is not None:
            if action == "n":
                url = _offset_url(url)
                #print("new url:", url)
                soup = make_soup(url)
            elif action == "p":
                url = _offset_url(url, operation="subtract")
                #print("new url:", url)
                soup = make_soup(url)
            elif action == 'r':
                action = None
                soup = make_soup(url)
            elif action == "a":
                return None
        D = _show(soup)
        selection, action = _select(D)
        if selection is not None:
            return selection




