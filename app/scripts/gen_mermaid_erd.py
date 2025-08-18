#!/usr/bin/env python3
# scripts/gen_mermaid_erd.py
# Genera un diagrama Mermaid (classDiagram) desde los modelos SQLAlchemy.
# Requiere que tu app exponga create_app() y que app.extensions.db exista.

import inspect
from datetime import datetime
from typing import List
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import RelationshipProperty

from app import create_app
from app.extensions import db
import app.models as models  # tus __all__ deberían exportar clases modelo

def get_model_classes():
    # Toma las clases mapeadas del registry de SQLAlchemy (Flask-SQLAlchemy 3.x)
    classes = []
    for mapper in db.Model.registry.mappers:
        cls = mapper.class_
        # Solo clases definidas por ti (con __tablename__)
        if hasattr(cls, "__tablename__"):
            classes.append(cls)
    # Orden estable por nombre
    return sorted(classes, key=lambda c: c.__name__)

def fmt_type(coltype):
    # Representación simple del tipo
    t = coltype.__class__.__name__
    return t.replace("Integer", "int").replace("String", "str")

def column_lines(cls) -> List[str]:
    lines = []
    for name, attr in cls.__dict__.items():
        if isinstance(attr, Column):
            # Cuando declarativo clásico, attr es InstrumentedAttribute; robustez:
            continue
    # Usar mapper para columnas seguras
    mapper = cls.__mapper__
    for col in mapper.columns:
        colname = col.name
        ctype = fmt_type(col.type)
        flags = []
        if col.primary_key: flags.append("PK")
        if not col.nullable and not col.primary_key: flags.append("NN")
        if col.unique: flags.append("UQ")
        deco = f" ({','.join(flags)})" if flags else ""
        lines.append(f"    +{colname}: {ctype}{deco}")
    return lines

def relationship_edges(cls):
    edges = []
    mapper = cls.__mapper__
    for rel in mapper.relationships:  # type: RelationshipProperty
        target = rel.entity.entity.__name__
        # Cardinalidad aproximada
        if rel.uselist:
            card = '"many"'
        else:
            card = '"1"'
        # Lado opuesto
        backref = rel.back_populates or rel.backref or ""
        # Mermaid relación simple
        # Ej: ClassA "1" --> "many" ClassB : rel_name
        left = '"1"' if not rel.uselist else '"many"'
        right = '"many"' if rel.uselist else '"1"'
        label = rel.key
        edges.append((cls.__name__, target, left, right, label))
    return edges

def fk_edges(cls):
    # Alternativa: relaciones vía FK directas (por si no hay relationship declarada)
    edges = []
    for col in cls.__table__.columns:
        for fk in col.foreign_keys:
            target_table = fk.column.table.name
            # Buscar clase destino por __tablename__
            target_cls = None
            for c in get_model_classes():
                if getattr(c, "__tablename__", None) == target_table:
                    target_cls = c.__name__
                    break
            if target_cls:
                edges.append((cls.__name__, target_cls, '"many"', '"1"', f"{col.name}"))
    return edges

def main():
    app = create_app()
    with app.app_context():
        classes = get_model_classes()
        print("# BDD — Diagrama (autogenerado)\n")
        print("```mermaid")
        print("classDiagram")

        # Clases con atributos
        for cls in classes:
            print(f"  class {cls.__name__} {{")
            for line in column_lines(cls):
                print(line)
            print("  }")

        # Relaciones (preferir ORM, complementar con FKs)
        rel_pairs = set()
        for cls in classes:
            for a, b, left, right, label in relationship_edges(cls) + fk_edges(cls):
                sig = (a, b, label)
                if sig in rel_pairs:
                    continue
                rel_pairs.add(sig)
                print(f"  {a} {left} --> {right} {b} : {label}")

        print("```")
        print(f"\n_Generado: {datetime.utcnow().isoformat()}Z_")

if __name__ == "__main__":
    main()
