# pyeio

<br>
<div align="left">
<a href="https://harttraveller.github.io/pyeio" target="_blank">
<img src="https://raw.githubusercontent.com/harttraveller/pyeio/main/docs/assets/pyeio-large.png" height=20>
</a>
<a href="https://pypi.org/project/pyeio/" target="_blank">
<img src="https://img.shields.io/pypi/v/pyeio" height=20>
</a>
<a href="https://github.com/harttraveller/pyeio/blob/main/LICENSE" target="_blank">
<img src="https://img.shields.io/badge/license-MIT-blue" height=20>
</a>
</div>

<br>

Short for `Py`thon `E`asy `I`nput `O`utput, `pyeio` is a python library meant to simplify file IO processes.

## Installation

Install format support with: `pip install 'pyeio[<formats>]'`

EG:

```sh
pip install 'pyeio[json,toml]'
```

## User Story

```python
import pyeio as po

po.load("path or url")

po.save(data, "path")
```