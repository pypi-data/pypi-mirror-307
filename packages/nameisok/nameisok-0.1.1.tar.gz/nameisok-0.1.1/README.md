# nameisok

**nameisok** is a Python package that checks the availability of package names on PyPI. This tool is especially useful for developers looking to publish new packages and wanting to ensure their desired name is unique.

## Installation

To install **nameisok**, simply run:

```bash
pip install nameisok
```


```bash
nameisok pandas,example

```

```plaintext
❌ `example` is already taken.
🎉 Wow! `my_package` is available!
❌ `nameisok` is already taken.

```