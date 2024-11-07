## Installing Prismstudio

### PyPI
PrismStudio can be installed via pip from [PyPI](https://pypi.org/project/prismstudio/)

```shell
pip install prismstudio
```

### Conda
Add Conda Forge Channel (if not added): To ensure that PrismStudio's dependencies can be found, add the Conda Forge channel to your Conda configuration. Run the following command:

```shell
conda config --add channels conda-forge
```

Install PrismStudio: Once you've added the Conda Forge channel, you can install PrismStudio using the following command:

```shell
conda install -c prism39 prismstudio
```

### Supported Python Versions:
Python 3.8
Python 3.9
Python 3.10
Python 3.11

### Supported Operating Systems and Architectures:
Windows x86
Linux x86
MacOSX arm


Trouble Installing?: If you encounter any issues during the installation process, please contact our support team at support@prism39.com for assistance. Our dedicated support staff will be happy to help you resolve any installation-related problems.


## Importing PrismStudio

To utilize the functionality of PrismStudio, you can import it into your Python code using the following line:

```python
import prismstudio as ps
```

```{tip}
We have chosen to abbreviate the imported name to `ps` to improve the readability of code that uses PrismStudio. This is a common convention that is widely accepted, so it's recommended that you follow it to ensure that your code can be easily understood by others.
```