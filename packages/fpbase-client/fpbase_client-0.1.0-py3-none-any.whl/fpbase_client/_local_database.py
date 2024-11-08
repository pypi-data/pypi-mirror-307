"""SQLite database management for FPBase data caching."""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional


class FPBaseDB:
    """SQLite database manager for FPBase data."""

    def __init__(self, db_path: str = None):
        """Initialize database connection and create tables if they don't exist.

        Args:
            db_path: Path to SQLite database file. If None, creates in this package's directory
        """
        if db_path is None:
            db_path = str(Path(__file__).parent / "fpbase_cache.db")

        self.conn = sqlite3.connect(db_path)
        # Enable dictionary access to rows
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        """Create proteins and spectra tables if they don't exist."""
        with self.conn:
            # Create proteins table with expanded schema
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS proteins (
                    uuid TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    slug TEXT NOT NULL,
                    seq TEXT,
                    ipg_id TEXT,
                    genbank TEXT,
                    uniprot TEXT,
                    pdb JSON,
                    agg TEXT,
                    switch_type TEXT,
                    states JSON,
                    transitions JSON,
                    doi TEXT
                )
            """)

            # Create spectra table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS spectra (
                    name TEXT NOT NULL,
                    slug TEXT NOT NULL,
                    spectra JSON NOT NULL
                )
            """)

            # Create indices for faster lookups
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_spectra_name ON spectra(name)"
            )
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_spectra_slug ON spectra(slug)"
            )

    def store_proteins(self, proteins: List[Dict]):
        """Store protein data in the database.

        Args:
            proteins: List of protein dictionaries from the API
        """
        with self.conn:
            self.conn.executemany(
                """INSERT OR REPLACE INTO proteins 
                   (uuid, name, slug, seq, ipg_id, genbank, uniprot, pdb, 
                    agg, switch_type, states, transitions, doi) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                [
                    (
                        p["uuid"],
                        p["name"],
                        p["slug"],
                        p.get("seq"),
                        p.get("ipg_id"),
                        p.get("genbank"),
                        p.get("uniprot"),
                        json.dumps(p.get("pdb", [])),
                        p.get("agg"),
                        p.get("switch_type"),
                        json.dumps(p.get("states", [])),
                        json.dumps(p.get("transitions", [])),
                        p.get("doi"),
                    )
                    for p in proteins
                ],
            )

    def store_spectra(self, spectra_data: List[Dict]):
        """Store spectra data in the database.

        Args:
            spectra_data: List of spectra dictionaries from the API
        """
        with self.conn:
            self.conn.executemany(
                "INSERT OR REPLACE INTO spectra (name, slug, spectra) VALUES (?, ?, ?)",
                [
                    (s["name"], s["slug"], json.dumps(s["spectra"]))
                    for s in spectra_data
                ],
            )

    def get_all_proteins(self) -> List[Dict]:
        """Retrieve all proteins from the database.

        Returns:
            List of protein dictionaries
        """
        with self.conn:
            cursor = self.conn.execute(
                """SELECT uuid, name, slug, seq, ipg_id, genbank, uniprot, 
                          pdb, agg, switch_type, states, transitions, doi 
                   FROM proteins"""
            )
            return [
                {
                    "uuid": row["uuid"],
                    "name": row["name"],
                    "slug": row["slug"],
                    "seq": row["seq"],
                    "ipg_id": row["ipg_id"],
                    "genbank": row["genbank"],
                    "uniprot": row["uniprot"],
                    "pdb": json.loads(row["pdb"]),
                    "agg": row["agg"],
                    "switch_type": row["switch_type"],
                    "states": json.loads(row["states"]),
                    "transitions": json.loads(row["transitions"]),
                    "doi": row["doi"],
                }
                for row in cursor
            ]

    def get_all_spectra(self) -> List[Dict]:
        """Retrieve all spectra from the database.

        Returns:
            List of spectra dictionaries
        """
        with self.conn:
            cursor = self.conn.execute("SELECT name, slug, spectra FROM spectra")
            return [
                {
                    "name": row["name"],
                    "slug": row["slug"],
                    "spectra": json.loads(row["spectra"]),
                }
                for row in cursor
            ]

    def is_populated(self) -> bool:
        """Check if the database is populated."""
        with self.conn:
            cursor = self.conn.execute("SELECT COUNT(*) FROM proteins")
            return cursor.fetchone()[0] > 0

    def close(self):
        """Close the database connection."""
        self.conn.close()

    def get_protein_by_exact_name(self, name: str) -> Optional[Dict]:
        """Retrieve a protein by its exact name.

        Args:
            name: The exact name of the protein to find

        Returns:
            Protein dictionary if found, None otherwise
        """
        with self.conn:
            cursor = self.conn.execute(
                """SELECT uuid, name, slug, seq, ipg_id, genbank, uniprot, 
                          pdb, agg, switch_type, states, transitions, doi 
                   FROM proteins 
                   WHERE name = ? COLLATE NOCASE""",  # Case-insensitive match
                (name,),
            )
            row = cursor.fetchone()

            if row:
                return {
                    "uuid": row["uuid"],
                    "name": row["name"],
                    "slug": row["slug"],
                    "seq": row["seq"],
                    "ipg_id": row["ipg_id"],
                    "genbank": row["genbank"],
                    "uniprot": row["uniprot"],
                    "pdb": json.loads(row["pdb"]),
                    "agg": row["agg"],
                    "switch_type": row["switch_type"],
                    "states": json.loads(row["states"]),
                    "transitions": json.loads(row["transitions"]),
                    "doi": row["doi"],
                }
            return None

    def search_proteins_by_name(self, search_term: str) -> List[Dict]:
        """Search for proteins where the name contains the search term.

        Args:
            search_term: String to search for within protein names

        Returns:
            List of matching protein dictionaries
        """
        with self.conn:
            cursor = self.conn.execute(
                """SELECT uuid, name, slug, seq, ipg_id, genbank, uniprot, 
                          pdb, agg, switch_type, states, transitions, doi 
                   FROM proteins 
                   WHERE name LIKE ? COLLATE NOCASE""",  # Case-insensitive search
                (f"%{search_term}%",),
            )

            return [
                {
                    "uuid": row["uuid"],
                    "name": row["name"],
                    "slug": row["slug"],
                    "seq": row["seq"],
                    "ipg_id": row["ipg_id"],
                    "genbank": row["genbank"],
                    "uniprot": row["uniprot"],
                    "pdb": json.loads(row["pdb"]),
                    "agg": row["agg"],
                    "switch_type": row["switch_type"],
                    "states": json.loads(row["states"]),
                    "transitions": json.loads(row["transitions"]),
                    "doi": row["doi"],
                }
                for row in cursor
            ]

    def find_proteins_by_name(self, name: str, exact: bool = False) -> List[Dict]:
        """Search for proteins by name.

        Args:
            name: The name to search for
            exact: If True, only return exact matches (case-insensitive)
                  If False, return all proteins containing the search term

        Returns:
            List of matching protein dictionaries. For exact matches,
            returns either empty list or list with single protein.
        """
        if exact:
            result = self.get_protein_by_exact_name(name)
            return [result] if result else []
        return self.search_proteins_by_name(name)

    def _get_spectrum_by_exact_name(self, name: str) -> Optional[Dict]:
        """Retrieve a spectrum by its exact name.

        Args:
            name: The exact name of the spectrum to find

        Returns:
            Spectrum dictionary if found, None otherwise
        """
        with self.conn:
            cursor = self.conn.execute(
                """SELECT name, slug, spectra 
                   FROM spectra 
                   WHERE name = ? COLLATE NOCASE""",
                (name,),
            )
            row = cursor.fetchone()

            if row:
                return {
                    "name": row["name"],
                    "slug": row["slug"],
                    "spectra": json.loads(row["spectra"]),
                }
            return None

    def _search_spectra_by_name(self, search_term: str) -> List[Dict]:
        """Search for spectra where the name contains the search term.

        Args:
            search_term: String to search for within spectrum names

        Returns:
            List of matching spectrum dictionaries
        """
        with self.conn:
            cursor = self.conn.execute(
                """SELECT name, slug, spectra 
                   FROM spectra 
                   WHERE name LIKE ? COLLATE NOCASE""",
                (f"%{search_term}%",),
            )

            return [
                {
                    "name": row["name"],
                    "slug": row["slug"],
                    "spectra": json.loads(row["spectra"]),
                }
                for row in cursor
            ]

    def find_spectra_by_name(self, name: str, exact: bool = False) -> List[Dict]:
        """Search for spectra by name.

        Args:
            name: The name to search for
            exact: If True, only return exact matches (case-insensitive)
                  If False, return all spectra containing the search term

        Returns:
            List of matching spectrum dictionaries. For exact matches,
            returns either empty list or list with single spectrum.
        """
        if exact:
            result = self._get_spectrum_by_exact_name(name)
            return [result] if result else []
        return self._search_spectra_by_name(name)

    def delete_DB(self):
        """Recreate the database tables."""
        with self.conn:
            self.conn.execute("DROP TABLE IF EXISTS proteins")
            self.conn.execute("DROP TABLE IF EXISTS spectra")
