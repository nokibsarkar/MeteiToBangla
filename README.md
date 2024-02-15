[![PyPI](https://github.com/nokibsarkar/meiteitobangla/actions/workflows/python-publish.yml/badge.svg)](https://github.com/nokibsarkar/meiteitobangla/actions/workflows/python-publish.yml)
# MeiteiToBangla
This Python module was created to facilitate the conversion of the Manipuri Language (`mni`) from the Meitei Mayek script to the Bengali script. The module is based on the Unicode standard for the Meitei Mayek script and the Unicode standard for the Bengali script. The module is designed to be used with Python 3.6 or later.
I kindly thank the following people for their help in creating this module:
1. [Haoreima](https://mni.wikipedia.org/wiki/User:Haoreima) for the Meitei Mayek to Bangla rules and the Meitei Mayek Unicode standard.
# Background
Meitei Mayek is the script used to write the Meitei language, which is spoken in the Indian state of Manipur. The script is based on the Bengali script, and the two scripts share many characters. However, there are some differences between the two scripts, and the Meitei Mayek script has some characters that are not present in the Bengali script. 
# Installation
You can install this module via pip as:
```sh
pip install -U meiteitobangla
```
# Usage
The module is accessible as `mtei2bangla`.
```python
from mtei2bangla import MeiteitoBangla
input_text = input('Please enter an example text')
output = MeiteitoBangla.transliterate(input_text)
```
Since version, 1.1.0, the `MeiteitoBangla` has two methods `setpreprocess` and `setpostprocess` to set the pre and post process functions. The `setpreprocess` method takes a function as an argument and the `setpostprocess` method takes a function as an argument. The function should take a string as an argument and return a string. The `transliterate` method will call the pre-process function before transliterating the text and the post-process function after transliterating the text. 
```python
from mtei2bangla import MeiteitoBangla
def custom_preprocess(text):
    return text
def custom_postprocess(text):
    return text
MeiteitoBangla.setpreprocess(custom_preprocess)
MeiteitoBangla.setpostprocess(custom_postprocess)
input_text = input('Please enter an example text')
output = MeiteitoBangla.transliterate(input_text)
```

# Known Limitations
1. It adds an `া` at the end of consonants if no diacritics are added. In most cases these are correct but in some foreign loan words, it is not correct. But as this module does not have any capability to distinguish between these words, it would add `া` at the end. Please use  `custom_end_func` (not implemented yet) to handle these correctly.
# License
Copyright (C) 2024 by Nokib Sarkar.
This module is licensed under the terms of the AGPLv3 license.
However, there is no restriction to use this module for the initial developer.
A copy of the license is included in the file [LICENCE.md](https://github.com/nokibsarkar/meiteitobangla/blob/main/LICENCE.md). If not, see [https://www.gnu.org/licenses/agpl-3.0.html](https://www.gnu.org/licenses/agpl-3.0.html).
