# %%
import multiprocessing
from pathlib import Path

import ifcopenshell
import ifcopenshell.geom

# import matplotlib.pyplot as plt

# TODO: Convert to CLI utility

# %% Input data
# TODO: Wrap it up to .yaml or .json input file
fpath = Path("../../ifc_examples_peikko/DummyModel.ifc")
pairs = [
    # ("IfcWall", "IfcWall"), # TODO: Ask Peikko about the wall-wall clashes and others
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


# %%
# TODO: Parallelize with concurrent.futures
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

len(clashes)
# %%
