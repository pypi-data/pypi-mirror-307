"""
bibliograpy process module
"""
import json
import logging
from argparse import Namespace
from pathlib import Path
from typing import Any

import bibtexparser
import yaml
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter

from bibliograpy.api import TYPES
from bibliograpy.api import Reference

LOG = logging.getLogger(__name__)


def _process(ns: Namespace):
    """config
    """
    LOG.info("dependencies")

    in_extension = ns.file.split('.')[-1]
    output_dir = Path(Path.cwd(), ns.output_dir)
    output_file = ns.output_file
    out_extension = output_file.split('.')[-1]
    scope_symbol = ns.scope if 'scope' in ns else None
    init_scope = ns.init_scope if 'init_scope' in ns else None

    LOG.info('open configuration file %s', ns.file)
    with open(ns.file, encoding=ns.encoding) as s:
        content = _read(s, extension=in_extension)

        with open(Path(output_dir, output_file), 'w', encoding=ns.encoding) as o:
            _write(o, extension=out_extension, content=content, scope_symbol=scope_symbol, init_scope=init_scope)

def _read(s, extension: str) -> list:
    """Reads the input bibliography file content."""

    if extension == 'yml':
        return yaml.safe_load(s)

    if extension == 'json':
        return json.load(s)

    if extension == 'bib':
        meta = {}
        content = []
        for e in bibtexparser.load(s).entries:
            meta['entry_type'] = e['ENTRYTYPE']
            meta[Reference.CITE_KEY_FIELD] = e['ID']
            del e['ENTRYTYPE']
            del e['ID']
            content.append({**meta, **e})
        return content

    raise ValueError(f'unsupported configuration format {extension}')

def _write(o, extension: str, content: list, scope_symbol: str | None, init_scope: str | None):
    """Writes the bibliography in the format specified by the provided extension."""

    if extension == 'py':

        scope: dict[str, Any] = {}

        o.write('from bibliograpy.api import *\n')
        o.write('\n')

        if init_scope is not None:
            o.write(f'{init_scope}\n')
            o.write('\n')

        for ref in content:
            if ref['entry_type'] in TYPES:
                o.write(f"{TYPES[ref['entry_type']].from_dict(ref, scope).to_py(scope_symbol=scope_symbol)}\n")
    elif extension in ['yml', 'yaml']:
        yaml.dump(content, o, sort_keys=False)
    elif extension in ['bib']:
        scope: dict[str, Any] = {}
        entries = []
        for ref in content:
            if ref['entry_type'] in TYPES:
                entries.append(TYPES[ref['entry_type']].from_dict(ref, scope).to_bib())
        db = BibDatabase()
        db.entries = entries
        writer = BibTexWriter()
        writer.order_entries_by = None
        bibtexparser.dump(bib_database=db, bibtex_file=o, writer=writer)
    elif extension in ['json']:
        json.dump(content, fp=o, sort_keys=False)
