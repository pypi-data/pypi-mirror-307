"""A Python client for the FPBase REST API."""

from .api import FPBaseAPI
from ._local_database import FPBaseDB

__version__ = "0.1.1"

# Initialize database and populate with data
db = FPBaseDB()
api = FPBaseAPI()


# Populate database with initial data
# only if the database is empty
def populate_DB():
    if not db.is_populated():
        db.store_proteins(api.get_all_proteins())
        db.store_spectra(api.get_all_spectra())


populate_DB()
find_proteins_by_name = db.find_proteins_by_name
find_spectra_by_name = db.find_spectra_by_name


# reinstall database
def reinstall_DB():
    db.delete_DB()
    populate_DB()


__all__ = [
    "FPBaseAPI",
    "FPBaseDB",
    "find_proteins_by_name",
    "find_spectra_by_name",
    "reinstall_DB",
]
