# kps9566py

KPS9566 encoding for Python 3

## Installation

```bash
pip install kps9566
```

## Example

```python
import kps9566

text = '아름다운 우리 나라'
print(text.encode('kps9566'))

data=b'\xb9\xc8\xb1\xfd\xb2\xf7 \xbc\xbf\xb0\xea'
print(data.decode('kps9566'))

```
