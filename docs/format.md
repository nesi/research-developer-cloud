`# Header 1`

# Header 1


More info about formatting here.
https://squidfunk.github.io/mkdocs-material/reference/


`## Header 2`

## Header 2

`### Header 3`

### Header 3

`#### Header 4`

#### Header 4

`**bold**`
**bold**

`_italic`
_italic_

```md
!!! info
    This is a test admonation.
```

!!! info
    This is a test admonation.
!!! note
!!! abstract
!!! info
!!! tip
!!! success
!!! question
!!! warning
!!! failure
!!! danger
!!! bug
!!! example
!!! quote

```md
=== "Tab One"
    someting in the tab
=== "Tab two"
    something else
```

=== "Tab One"
    someting in the tab
=== "Tab two"
    something else

```md
\```py
import somepackage

formatting = True
if formatting:
    Print(formatting) # A comment
\```
``` 

```python
import somepackage

formatting = True
if formatting:
    Print(formatting) # A comment
```

```md
![This is an image]("assets/images/3rgk_assembly-1.jpeg")
```

![This is an image]("assets/images/3rgk_assembly-1.jpeg")

```md
[External Link]("https://example.com")

```

[External Link]("https://example.com")

```md
[Internal Link]("General/Announcements")

```

[Internal Link]("General/Announcements")

```md
[Hover over me](https://example.com "I'm a link with a custom tooltip.")
```

[Hover over me](https://example.com "I'm a link with a custom tooltip.")


```md
Acroynym should be automatically tooltipped e.g. MPI.
```

Acroynym should be automatically tooltipped e.g. MPI.


{{ macros_info() }}


### Admonation

!!! type
    Something


### Content Tabs

Look like this

```
=== "Tab One"
    someting in the tab
=== "Tab two"
    something else
```

## Code Formatting

### Blocks

```py
import tensorflow as tf
import numpy as np 
```

Preferablyer

```py title="myScript.py"
import tensorflow as tf
import numpy as np 
```

All available lexers
https://pygments.org/docs/lexers/

### Inline

The command `ls -latr`

Or preferably

This codeblock '#!bash echo "is inline"

### Snippet from another file.

```md
--8<-- "../../includes/images/glossary/.dictionary.md"
```
