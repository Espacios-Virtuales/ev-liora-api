#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera un diagrama Mermaid (classDiagram) directamente desde la BDD actual.
Usa SQLAlchemy Inspector para reflejar tablas, columnas, PK/UQ/NN y FKs.
Funciona con Postgres/SQLite/etc. según DATABASE_URL.

Uso:
  python scripts/gen_mermaid_from_db.py \
    --url "$DATABASE_URL" \
    --out docs/diagrams/bdd.md \
    --schema public
"""

import argparse
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.inspection import inspect

def guess_cardinality(fk):
    # Por simplicidad: tabla hija "many" -> tabla padre "1"
    return '"many"', '"1"'

def fmt_type(t):
    # Nombre legible de tipo
    # p.ej. UUID, VARCHAR, INTEGER -> uuid, str, int
    name = str(t)
    lower = name.lower()
    if "uuid" in lower: return "uuid"
    if "int" in lower: return "int"
    if "float" in lower or "double" in lower or "numeric" in lower or "decimal" in lower: return "float"
    if "bool" in lower: return "bool"
    if "date" in lower or "time" in lower: return "datetime" if "time" in lower else "date"
    if "text" in lower: return "text"
    if "json" in lower: return "json"
    return "str"  # fallback

def collect_schema(url, schema=None):
    engine = create_engine(url)
    insp = inspect(engine)
    dialect = make_url(url).get_backend_name()

    # Listar tablas (en Postgres/otros puede requerir schema)
    if schema and hasattr(insp, "get_table_names"):
        tables = insp.get_table_names(schema=schema)
    else:
        tables = insp.get_table_names()

    data = []
    for table in sorted(tables):
        cols = []
        uniques = set()
        pks = set()

        pkc = insp.get_pk_constraint(table, schema=schema)
        if pkc and pkc.get("constrained_columns"):
            pks = set(pkc["constrained_columns"])

        for uq in insp.get_unique_constraints(table, schema=schema) or []:
            for c in uq.get("column_names", []) or []:
                uniques.add(c)

        for c in insp.get_columns(table, schema=schema):
            name = c["name"]
            ctype = fmt_type(c["type"])
            flags = []
            if name in pks: flags.append("PK")
            if (not c.get("nullable", True)) and (name not in pks): flags.append("NN")
            if name in uniques: flags.append("UQ")
            deco = f" ({','.join(flags)})" if flags else ""
            cols.append(f"    +{name}: {ctype}{deco}")

        # FKs
        fks = []
        for fk in insp.get_foreign_keys(table, schema=schema) or []:
            # Puede haber FKs compuestas; listamos una por columna
            referred_table = fk.get("referred_table")
            referred_schema = fk.get("referred_schema") or schema
            for lc, rc in zip(fk.get("constrained_columns", []),
                              fk.get("referred_columns", [])):
                fks.append({
                    "local_col": lc,
                    "remote_table": referred_table,
                    "remote_col": rc,
                    "remote_schema": referred_schema,
                })

        data.append({
            "table": table,
            "columns": cols,
            "fks": fks
        })
    return data

def write_mermaid(md_path, schema_data, title="BDD — Diagrama (autogenerado)"):
    os.makedirs(os.path.dirname(md_path), exist_ok=True)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write("```mermaid\n")
        f.write("classDiagram\n")

        # Clases + atributos
        for item in schema_data:
            tbl = item["table"]
            f.write(f"  class {tbl} {{\n")
            for line in item["columns"]:
                f.write(line + "\n")
            f.write("  }\n")

        # Relaciones (FKs)
        # Evitar duplicados (A.col -> B.col)
        seen = set()
        for item in schema_data:
            a = item["table"]
            for fk in item["fks"]:
                b = fk["remote_table"]
                label = fk["local_col"]
                key = (a, b, label)
                if key in seen:
                    continue
                seen.add(key)
                left, right = guess_cardinality(fk)
                f.write(f"  {a} {left} --> {right} {b} : {label}\n")

        f.write("```\n")
        f.write(f"\n_Generado: {datetime.utcnow().isoformat()}Z_\n")

def main():
    ap = argparse.ArgumentParser(description="Genera Mermaid classDiagram desde la BDD actual.")
    ap.add_argument("--url", default=os.getenv("DATABASE_URL"), help="DATABASE_URL (SQLAlchemy).")
    ap.add_argument("--schema", default=None, help="Schema (p.ej. public en Postgres).")
    ap.add_argument("--out", default="docs/diagrams/bdd.md", help="Ruta de salida .md")
    ap.add_argument("--title", default="BDD — Diagrama (autogenerado)", help="Título en el .md")
    args = ap.parse_args()

    if not args.url:
        raise SystemExit("Falta --url o variable de entorno DATABASE_URL.")

    schema_data = collect_schema(args.url, schema=args.schema)
    write_mermaid(args.out, schema_data, title=args.title)
    print(f"OK -> {args.out}")

if __name__ == "__main__":
    main()
