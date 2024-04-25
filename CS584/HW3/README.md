# Instructions for Homework Coding

## Environment

### Python Installation

Python 3.8+ (Recommended)

#### Windows

- Windows version: Windows 7+
- Download link:
  - Python 3.8.9 (32-bit): [https://www.python.org/ftp/python/3.8.9/python-3.8.9.exe](https://www.python.org/ftp/python/3.8.9/python-3.8.9.exe)
  - Python 3.8.9 (64-bit): [https://www.python.org/ftp/python/3.8.9/python-3.8.9-amd64.exe](https://www.python.org/ftp/python/3.8.9/python-3.8.9-amd64.exe)
  - Or you can choose other versions from [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
- Installation guide: [https://www.youtube.com/watch?v=i-MuSAwgwCU](https://www.youtube.com/watch?v=i-MuSAwgwCU)
  - Don't forget to add Python to the system path

#### macOS

- Download link:
  - Python 3.8.9 (64 bit): [https://www.python.org/ftp/python/3.8.9/python-3.8.9-macosx10.9.pkg](https://www.python.org/ftp/python/3.8.9/python-3.8.9-macosx10.9.pkg)
  - Or you can choose other versions from [https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/)
- Installation guide: [https://www.youtube.com/watch?v=TgA4ObrowRg](https://www.youtube.com/watch?v=TgA4ObrowRg)

#### Ubuntu

- For Ubuntu version >= 20.04, Python 3.8 is already installed with system and is the default Python version.


## IDE

### PyCharm

Link: [https://www.jetbrains.com/pycharm/](https://www.jetbrains.com/pycharm/).

You can activate PyCharm by registering an account of Jetbrains using you Stevens email

### Jupyter Notebook

```console
# Install
pip install jupyterlab

# Run
jupyter-lab
```

### Google Colab

Link: [https://colab.research.google.com/](https://colab.research.google.com/)

Google Colab is an online Python notebook that is similar to jupyter notebook. You can use GPU or even TPU here.


## Install Packages and Run Python Code

### Virtualenv

Link: [https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html)

Using virtualenv is recommended. It can let you maintain different python package requirements independently for different projects.

To create virtualenv, run
```console
python -m venv venv
```

It will create a sub-folder `venv` in the current folder.

To activate venv, run
```console
# Windows Powershell
.\venv\Scripts\Activate.ps1

# Windows cmd
.\venv\Scripts\activate.bat

# Ubuntu and macOS user
source ./venv/bin/activate
```

After activate virtualenv, run
```console
python -m pip install --upgrade pip
```

To deactivate venv, run
```console
deactivate
```
