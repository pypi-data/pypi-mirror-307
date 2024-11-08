# py-gltf

Library for processing GLTF files.

## Installation

```
pip install gltf
```

## Usage

```
import uuid
from gltf import GLTF
g = GLTF.load('examples/test.glb')

for tex in g.textures:
    tex.name += ' ' + str(uuid.uuid4())
    tex.source.name += ' ' + str(uuid.uuid4())

g.save()

```

## Building

```commandline
python setup.py sdist
twine upload dist/*
```
