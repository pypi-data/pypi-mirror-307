# Uppsala pyub

Use Uppsala University's library catalog from the command line or script searches by using this package as a module.

## installation

Install with pip

```
pip install uppsala-pyub
```

## Usage

### CLI

Call pyub from the command line with a specific instruction (currently only `fetch_bibtext` / `bib` is implemented).

![usage example 1](https://raw.githubusercontent.com/BobBorges/uppsala-pyub/refs/heads/main/docs/img/usage-example-1.png) 

Check the available options with `pyub --help` 

![help](https://raw.githubusercontent.com/BobBorges/uppsala-pyub/refs/heads/main/docs/img/help.png)

...and create advanced searches.

![usage example 2](https://raw.githubusercontent.com/BobBorges/uppsala-pyub/refs/heads/main/docs/img/usage-example-2.png)


### As a Module

Pyub can also be used in scripting. See the api documentation [here](https://bobborges.github.io/uppsala-pyub/). For example:


```python
from uppsala_pyub.bibtex import make_bibtex
from uppsala_pyub.query import (
	cap_query,
	run_search,
)
from uppsala_pyub.handle_results import display_results



queries = [
	{
		"creator": "marcus garvey"
	},
	{
		"creator": "muysken pieter",
		"resource_type": "books",
		"creation_from": "1999"
		"creation_to": "2003"
	}
]
for q in queries:
	query = cap_query(q)
	result_soup, url = run_search(**query)
	selection = display_results(result_soup, url)
	if selection is not None:
		bibtex_key = make_bibtex(selection, output_location='./')
```


When used in a script, `display_results()` requires the same user interaction as cli usage.

### Implemented "instructions"

#### `fetch_bibtex`

The `fetch_bibtex` instruction constructs a bibtex file from the data returned by the library's search url and saves it in the current working directory. The bibtex key is the same as the filename without the `.bib` extension. Keys are constructed to be human readable and recognizable by the resource creator and year.

N.b. There are currently no checks in place to prevent pyub from overwriting an existing entry, so take care to quarantine bibtex downloads and manually adjust the key/filename as necessary to disambiguate works by a single author in the same year.

### Planned "instructions"

#### `generate_citation`

Generate a formatted citation for the selected resource in a given referencing style.

#### `list_links`

Get a list of urls to / about the selected resource.

#### `show_physical_locations`

List UU libraries that hold the selected resource.
