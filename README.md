# Python Extension Framework

This is a framework for building [AWS Lambda Extensions](https://aws.amazon.com/blogs/compute/introducing-aws-lambda-extensions-in-preview/).

## Quickstart

```bash
$ pip install lef
```

To get started you can use the default `Extension` class, or extend it.

Example:

```python
import lef

def handler(event):
    print(event)

extension = lef.Extension()
extension.register([lef.EventType.INVOKE], handler)
```

## Development

Install Dependencies

```bash
$ poetry install --dev
```

Bump Version

```bash
$ poetry run bumpversion <VERSION LEVEL>
```
