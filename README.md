# ICA for demixing images

## Motivation

This is a very simple example of how to use FastICA of
[scikit-learn](https://scikit-learn.org/stable/index.html)
to demix images that were linearly mixed.
It shows how good the results can be for structured high-dimensional signals despite the fact that
the underlying independence hypotheses of ICA do not respect the two-dimensional structure of the data
(each image is stacked into a vector) and the sequential nature of the data (each signal is a random variable
and the observed values are i.i.d. samples).

Why do we need a GUI?
Well, ICA cannot recover the right magnitudes of the independent components.
Hence some images are "inverted".
The GUI lets you invert the color map for each image separately.

## Dependencies
You will need python 3 with [scikit-learn](https://scikit-learn.org/stable/index.html) and
[PyQt5](https://pypi.org/project/PyQt5/).

# Code
I borrowed the core code
from [Blind source separation using FastICA](https://scikit-learn.org/stable/auto_examples/decomposition/plot_ica_blind_source_separation.html#sphx-glr-auto-examples-decomposition-plot-ica-blind-source-separation-py)

## Usage
```
python3 main.py --help
```
will tell you everything about the usage.

It is as simple as that: You provide the pictures and the seed for the mixing matrix:
```
python3 main.py --seed 1234 --file city.jpg bumper.jpg raisin.jpg flats.jpg
```

## Results

```
python3 main.py
```
Defaults will be assumed, and you get
 
![Demo in 2D](https://github.com/ldv1/ICA_for_demixing_images/blob/master/defaults.png)

The top row depicts the unmixed images (ground truth),
the middle row shows the mixed images,
and the bottom row gives the results of the demixing with ICA.

The second picture from the left at the bottom is inverted.

## Authors
Laurent de Vito

## License
All third-party libraries are subject to their own license.

<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License</a>.
