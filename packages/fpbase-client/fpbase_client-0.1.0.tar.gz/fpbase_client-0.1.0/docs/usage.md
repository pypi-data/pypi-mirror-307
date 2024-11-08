# Usage Guide

## Basic Usage

### Initialize the client

```python
from fpbase_client import FPBaseAPI, find_proteins_by_name, find_spectra_by_name
```

### Search for Proteins

```python
# Using the API client directly
api = FPBaseAPI()
proteins = api.search_by_name("GFP")  # Partial match
proteins = api.search_by_name("EGFP", partial_match=False)  # Exact match

# Using the local database (faster, works offline)
proteins = find_proteins_by_name("GFP")  # Partial match
proteins = find_proteins_by_name("EGFP", exact=True)  # Exact match
```

### Get Spectra Data

```python
# Using the local database
spectra = find_spectra_by_name("EGFP", exact=True)
# returns a list of dictionaries with the following keys:
# name, slug, spectra
# spectra is a list of dictionaries with the following keys:
# state, ec, max, data: (state name in string, exctinction coefficient in M^-1 cm^-1, 
#                       wavelength at max excitation or emission based on state, 
#                       List[List[float, float]] representing the wavelength and 
#                       intensity of the spectrum (note: intensity is from 0-1))
```

### Get All Data

```python
# Get all proteins
all_proteins = api.get_all_proteins()

# Get all spectra
all_spectra = api.get_all_spectra()

# Reinstall local database
from fpbase_client import reinstall_DB
reinstall_DB()  # This will delete and repopulate the local cache
```

## Advanced Usage

### Custom Queries
For more specific searches, you can use the `get_proteins()` method with custom filters:

```python
# Find bright green proteins
proteins = api.get_proteins(
    name__icontains='green',
    default_state__qy__gte=0.7,
    default_state__brightness__gte=0.5
)
```

### Available Search Fields
The `get_proteins()` method supports various fields and lookups (see [FPBase API docs](https://fpbase.org/api/)):
- `name`: icontains, iendswith, istartswith, iexact
- `seq`: icontains, iendswith, istartswith, cdna_contains
- `default_state__ex_max`: around, range, lte, gte, exact
- `default_state__em_max`: around, range, lte, gte, exact
- `default_state__lifetime`: gte, lte, range, exact
- And many more...

### Rate Limiting
The client automatically handles rate limiting with a default delay of 0.5 seconds between requests. You can customize this:

```python
client = FPBaseAPI(rate_limit_delay=1.0)  # 1 second between requests
```





