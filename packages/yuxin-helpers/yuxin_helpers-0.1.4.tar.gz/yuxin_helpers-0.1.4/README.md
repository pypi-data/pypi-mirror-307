# yuxin_helpers

Yuxin's helper package with utilities for diverse tasks.

## Installation

```bash
pip install yuxin_helpers
```

## Usage

### Convert RGB to Hex

```python
from yuxin_helpers import rgb_to_hex

print(rgb_to_hex(255, 0, 0))  # Output: '#ff0000'
```

### Convert Hex to RGB

```python
from yuxin_helpers import hex_to_rgb

print(hex_to_rgb('#ff0000'))  # Output: (255, 0, 0)
```

Here's an updated version of your `README.md` with the new function `truncate_colormap` added to the usage section:

---

# yuxin_helpers

Yuxin's helper package with utilities for diverse tasks.

## Installation

```bash
pip install yuxin_helpers
```

## Usage

### Convert RGB to Hex

```python
from yuxin_helpers import rgb_to_hex

print(rgb_to_hex(255, 0, 0))  # Output: '#ff0000'
```

### Convert Hex to RGB

```python
from yuxin_helpers import hex_to_rgb

print(hex_to_rgb('#ff0000'))  # Output: (255, 0, 0)
```

### Truncate a Colormap

```python
import matplotlib.pyplot as plt
import numpy as np
from yuxin_helpers import truncate_colormap

# Example usage
cmap = plt.get_cmap('viridis')
truncated_cmap = truncate_colormap(cmap, minval=0.2, maxval=0.8, n=200)

# Plotting to visualize the truncated colormap
plt.imshow(np.linspace(0, 1, 100).reshape(10, 10), cmap=truncated_cmap)
plt.colorbar()
plt.show()
```
