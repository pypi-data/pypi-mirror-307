# jupygcc

[![PyPI - Version](https://img.shields.io/pypi/v/jupygcc.svg)](https://pypi.org/project/jupygcc)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jupygcc.svg)](https://pypi.org/project/jupygcc)

-----

## Installation

```console
pip install jupygcc
```

## Usage

Load the extension.

````markdown
```{python}
#| echo: false
#| output: false
%load_ext jupygcc
```
````
Provides both `%gcc` line magic that takes a c filename as argument and `%%gcc`
cell magic that handle c code in the cell.

Line magic.

````markdown
```{python}
%gcc ex1/main.c
```
````

Cell magic.

````markdown
#include <stdio.h>
int somme(int n) {
  if (n <= 0)
    return 0;
  else
    return (n + somme(n - 1));
}
int main() {
  printf("u(%d= %d", 6, somme(6));
  return 0;
}
````
### Configuration

Currently, the kernel can't be configured and will always use:

- `-std=c99 -Wall` for C code
- Wrap the code in a ``main`` function if it doesn't already have one with:

  ```c
  #include <stdbool.h>
  #include <stddef.h>
  #include <stdint.h>
  #include <stdio.h>
  #include <stdlib.h>
  #include <math.h>
  ```

### Cell metadata

Currently, the only cell metadata handled is `stdin`.:

```{c}
//| stdin: 10
int n;
printf("How many lines? ");
scanf("%d", &n);
printf("\n%d lines\n");
```

## Development

- Test: `hatch run test`
- Coverage: `htach run coverage`
- 
## License

`jupygcc` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
