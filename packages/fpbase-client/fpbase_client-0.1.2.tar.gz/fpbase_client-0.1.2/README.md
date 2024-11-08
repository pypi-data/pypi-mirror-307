# FPBase Client

A Python client for the FPBase REST API with local SQLite caching.

## Installation

```bash
git clone https://github.com/joemans3/fpbase-client.git
cd fpbase-client
pip install -e .
```

## Basic Usage

```python
from fpbase_client import FPBaseAPI, find_proteins_by_name, find_spectra_by_name

# Using the API client directly
api = FPBaseAPI()
proteins = api.search_by_name("GFP")  # Partial match
proteins = api.search_by_name("EGFP", partial_match=False)  # Exact match

# Using the local database (faster, works offline)
proteins = find_proteins_by_name("GFP")  # Partial match
proteins = find_proteins_by_name("EGFP", exact=True)  # Exact match

# Advanced API queries
# For advanced users who need more specific queries, use get_proteins() with filters
proteins = api.get_proteins(
    name__icontains='green',
    default_state__qy__gte=0.7,
    default_state__brightness__gte=0.5
)

# Find spectra
spectra = find_spectra_by_name("EGFP", exact=True)
# returns a list of dictionaries with the following keys:
# name, slug, spectra
# spectra is a list of dictionaries with the following keys:
# state, ec, max, data: (state name in string, exctinction coefficient in M^-1 cm^-1, wavelength at max excitation or emission based on state, List[List[float, float]] representing the wavelength and intensity of the spectrum (note: intensity is from 0-1))


# Get all data
all_proteins = api.get_all_proteins()
all_spectra = api.get_all_spectra()

# Reinstall local database
from fpbase_client import reinstall_DB
reinstall_DB()  # This will delete and repopulate the local cache
```

## Available Methods

### API Methods
- `search_by_name(name, partial_match=True)`: Search proteins by name
- `get_proteins(**kwargs)`: Advanced protein search with filters
- `get_all_proteins()`: Get all proteins
- `get_all_spectra()`: Get all spectra

### Local Database Methods
- `find_proteins_by_name(name, exact=False)`: Search proteins by name using local cache
- `find_spectra_by_name(name, exact=False)`: Search spectra by name using local cache
- `reinstall_DB()`: Delete and repopulate the local database cache

## Advanced Search Fields

The `get_proteins()` method supports various fields and lookups (see [FPBase API docs](https://www.fpbase.org/api/)):

- `name`: icontains, iendswith, istartswith, iexact
- `seq`: icontains, iendswith, istartswith, cdna_contains
- `default_state__ex_max`: around, range, lte, gte, exact
- `default_state__em_max`: around, range, lte, gte, exact
- `default_state__lifetime`: gte, lte, range, exact
- And many more...

Example:
```python
proteins = api.get_proteins(
    name__icontains='green',
    default_state__qy__gte=0.7,
    primary_reference__year__gte=2020
)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
