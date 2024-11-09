# pyeio

<br>
<div align="left">
<a href="https://pypi.org/project/pyeio/" target="_blank">
<img src="https://img.shields.io/pypi/v/pyeio" height=20>
</a>
<a href="https://github.com/harttraveller/pyeio/blob/main/LICENSE" target="_blank">
<img src="https://img.shields.io/badge/license-MIT-blue" height=20>
</a>
</div>
<br>

Short for `Py`thon `E`asy `I`nput `O`utput, `pyeio` is a python library meant to simplify file IO processes.

This is currently very unstable, but the idea is to capture as much functionality as possible, consolidate it, simplify it, minimize dependencies (further down the line) and optimize stuff with rust.

In addition to a python library, it also comes with a CLI - currently very restricted but somewhat optimized, intended to replicate functionality found across other system utilities and CLIs.

For instance, to count the number of lines in a 15 GB `items.jsonl` file one could run:

```sh
wc -l items.jsonl
```

Which takes 12.03s to run (on my machine). Alternatively:

```sh
eio wc -l items.jsonl
```

Which runs in 1.14s.

I suspect things will be very unstable for another few months.

<!-- ## Installation

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


## Developer


## Links

- https://pyo3.rs
- https://www.maturin.rs -->