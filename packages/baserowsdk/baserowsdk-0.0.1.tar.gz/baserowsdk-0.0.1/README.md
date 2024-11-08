# Baserowsdk


# Requirements

python3.8 +

# Installation

```shell
pip install --upgrade baserowsdk
```

# Getting started

## Example

```python
from baserowsdk.client import Client

client = Client(token="xxxx", base_url="http://192.168.40.220")
rows = client.rows(table_id=182)
print(rows)

```