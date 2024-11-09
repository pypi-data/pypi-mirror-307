# HyTek

Parses, reads, and writes HyTek meet entries and results files.

## File Format Support
| Format | Reading | Writing |               Notes                |
|:------:|:-------:|:-------:|:----------------------------------:|
|  .hy3  |    ✅    |    ❌    | Only tested with meet result files |
|  .sd3  |    ❌    |    ❌    |                                    |
|  .cl2  |    ❌    |    ❌    |                                    |
|  .ev3  |    ❌    |    ❌    |                                    |
|  .hyv  |    ❌    |    ❌    |                                    |

## Installation

```bash
pip install hytek
```

## Usage

```python
import hytek

# for a .hy3 file
file = hytek.Hy3File("file.hy3")
file.read()

# .hy3 in a zip file
file = hytek.Hy3File("file.hy3")  # if left blank for zip files, will detect first .hy3 file
file.read_zip("test.zip")
```