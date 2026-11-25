#!/usr/bin/env python3
"""Copy the entry image to /output/entry.png (stdlib only, no network)."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"

os.makedirs("/output", exist_ok=True)
shutil.copyfile(SRC, DST)
print("wrote", DST)
