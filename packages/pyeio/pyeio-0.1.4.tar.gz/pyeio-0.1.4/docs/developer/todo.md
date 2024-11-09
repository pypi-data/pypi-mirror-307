# Todo

! a lot of these features should be split into different libraries/packages, this one should have minimal dependencies and just be really good at one thing


## Requirements

## Stretch Goals

- Reduce external dependencies to > n (some low number) for all file formats
- Benchmark and try to speed up all operations.
- Use Result

## Features

### Dependencies




### Security

- pdfid - security analysis and deactivation of potentially malicious pdfs
- detection of whether archive is zip bomb
- google safebrowsing integration for downloading files, urls
- scrub/randomize exif metadata from images
- scrub/randomize generic metadata in files
- add some encryption utilities

### Analysis

- in addition to estimating the number of lines in an uncompressed file, I should create an estimator for compressed files that factors in convergence of the compression ratio of text

### Unsorted

- check file integrity (hashes)
- check data integrity (parsable according to spec)
- fix data integrity (attempt to identify problem in corrupted data and fix it)
- get file size (raw and when in archive)
    - rough estimation for large files, return est. range?
    - compute with certainty (much slower)
- get in memory data size (pympler)
- estimate number of text lines in file
    - rough estimation for large files, return est. range?
    - compute with certainty (much slower)
        - implement on disk cache of file/data hash so computation is accelerated for same file?
- estimate unpacked file size
- get file metadata (exif data, on disk metadata, pdf metadata)
- search disk for file
- use magic, chardet, langdetect(?) for identification of data/file properties/types
- (generic util) look at file/data entropy
- when downloading files, implement on disk caching for data based on hashes to avoid duplicative downloads?
    - would need to allow bypass
- pydantic schema generation and validation
- automated data cleaning
- when there isn't any file extension, and the automatic loaders are used, the system should try and use python-magic to identify the file format
- add feature to write msgspec/pydantic models from data
- add feature to dynamically generate in memory pydantic models for validation
    - jsonschema validation?
- do file format analysis using stack exchange sites/stack overflow data
- gather file metadata
- move files
- rename files
- grep in files/across files
- search files system
- get metadata about file system
- estimate/calc files/data size
- estimate/calc num lines
- estimate/calc num blocks
- estimate/calc num chars
- add ability to get hash of in memory object to `File` for use in both memory cache, and disk cache


### Maybe?

- include CLI for various tools (typer?)
    - would definitely be useful for accessing rust code that is just useful and accelerated - eg: for checking the number of lines in a file
- chaining of operations (pipe?)
- optional integration of web module with proxy service?
- fake user agent generation
- web crawling/evaluation with llm?
- create hierarchy of format sets - svg can be loaded by xml parser, md by txt, but pdf not by json, etc
- find files with data (search system), allow customization for handler that returns bool for positive identification
    - extend to crawling web/sites/domains
- search engine for files on local machine
- search for images, use local vision model to assess contents
    - create and maintain index/cache to make future searches faster
    - also can do for text and code
- search for and handle (delete, export, list, etc) duplicates
- crawl domain to find files, add evaluator?
- encryption utilities
- host system analysis utilities
- system forensics and inference utilities
- add ability to detect link format for download and traverse to correct link/object, eg:

```python
# this should download video not html of youtube page
web.intelligent_download(url="https://www.youtube.com/watch?v=eHzoTLwx01E", path="CES 2024.mp4")

# this should download file at https://raw.githubusercontent.com/harttraveller/pyeio/refs/heads/main/data/json/books.json
web.intelligent_download(url="https://github.com/harttraveller/pyeio/blob/main/data/json/books.json", path="books.json")
```

---

local disk operations:
    path to mem (return) : open
    path to mem (yield): read
    mem to path (create/overwrite): save
    mem to path (modify): ...

web operations:
    url to mem (return) : load
    url to mem (yield) : stream
    url to disk : pull


- to mem (open)
    - from disk (path) | disk_open | **load**
    - from web (url) | web_open | **wload**
- to disk (save)
    - from mem (object) | mem_save (save)
    - from web (url) | web_save (wsave)
    

path/to mem
- 
url/to mem
data/to disk
url/to disk

