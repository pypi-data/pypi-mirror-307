# PyColorate
A lightweight python library to easily colorate text

## Features

- Support for multiple color gradients.
- Various gradient directions (horizontal, vertical, diagonal, etc.).
- Easy integration with terminal applications.
- Customizable wave effect for dynamic visual output.

## Installation

You can install the package via pip:

```bash
pip install PyColorate
```

## Usage


### Basic Usage
```python
from PyColorate.pycolor import Colorate, ColorGradients, Direction

# Initialize the Colorate system
colorate = Colorate()

# Apply a gradient to a simple text
text = "Hello, World!"
gradient_text = colorate.gradient_text(text, ColorGradients.RED_GRADIENTS)
print(gradient_text)
```

## Using two gradients
```python
from PyColorate.pycolor import Colorate, ColorGradients, Direction

colorate = Colorate()

# Apply a gradient from red to blue
text = "Gradient Text"
gradient_text = colorate.gradient_text(text, ColorGradients.RED_GRADIENTS, ColorGradients.BLUE_GRADIENTS)
print(gradient_text)
```

# Contributing
If you'd like to contribute to this project, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

# License
This project is licensed under the MIT License - see the LICENSE file for details.