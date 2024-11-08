### python binding for salt

#### Usage

```python
from pysaltrouting import pysalt
from pathlib import Path
post_file = str(Path(pysalt.__file__).parent / 'data/POST9.dat')
powv_file = str(Path(pysalt.__file__).parent / 'data/POWV9.dat')
pysalt.net_file(<net/file/path>, <epsilon>, post_file, powv_file)
```

#### Install

`pip install pysaltrouting`