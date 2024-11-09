# %%
import multiprocessing
from pathlib import Path

import ifcopenshell
import ifcopenshell.geom
import numpy as np
import pandas as pd

# import matplotlib.pyplot as plt

# TODO: Convert to CLI utility

# %% Input data
# TODO: Wrap it up to .yaml or .json input file
fpath = Path("../../ifc_examples_peikko/One_Section.ifc")
pairs = [
    ("IfcWall", "IfcWall"),  # TODO: Ask Peikko about the wall-wall clashes and others
    ("IfcWall", "IfcBeam"),
    ("IfcWall", "IfcColumn"),
    ("IfcBeam", "IfcBeam"),
    ("IfcBeam", "IfcColumn"),
    ("IfcColumn", "IfcColumn"),
]
tolerance = 0.002  # TODO: Research the tolerance value


# %%
model = ifcopenshell.open(fpath)
tree = ifcopenshell.geom.tree()
settings = ifcopenshell.geom.settings()
iterator = ifcopenshell.geom.iterator(settings, model, multiprocessing.cpu_count())
if iterator.initialize():
    while True:
        # Use triangulation to build a BVH tree
        tree.add_element(iterator.get())

        # Alternatively, use this code to build an unbalanced binary tree
        # tree.add_element(iterator.get_native())

        if not iterator.next():
            break


# %% Find clashes
# TODO: Wrap it up to a function
clashes = []
for pair in pairs:
    clashes += list(
        tree.clash_intersection_many(
            model.by_type(pair[0]),
            model.by_type(pair[1]),
            tolerance=tolerance,
            check_all=True,
        )
    )


# %% Build DataFrame
def _get_material(element):
    material = None
    if element.HasAssociations:
        for assoc in element.HasAssociations:
            if assoc.is_a("IfcRelAssociatesMaterial"):
                material = assoc.RelatingMaterial.Name
                break
    return material


data = []
for clash in clashes:
    # Mean average of two points
    raw = [(lhs + rhs) / 2.0 for lhs, rhs in zip(clash.p1, clash.p2)]

    # Distance
    raw.append(clash.distance)

    # Object a
    raw.append(model.by_id(clash.a.id()).GlobalId)
    raw += _get_material(model.by_id(clash.a.id())).split("/", 1)

    # Object b
    raw.append(model.by_id(clash.b.id()).GlobalId)
    raw += _get_material(model.by_id(clash.b.id())).split("/", 1)

    # Clash type
    raw.append(["protrusion", "pierce", "collision", "clearance"][clash.clash_type])
    # IPA, HEA profile; L1.5mH200mm, W100mm
    data.append(raw)
df = pd.DataFrame(
    data,
    columns=[
        "x",
        "y",
        "z",
        "distance",
        "guid_a",
        "material_a",
        "spec_a",
        "guid_b",
        "material_b",
        "spec_b",
        "clash_type",
    ],
)
df

# %%
# [
#     ["protrusion", "pierce", "collision", "clearance"][clash.clash_type]
#     for clash in clashes
# ]
# IPA, HEA profile; L1.5mH200mm, W100
# %%
