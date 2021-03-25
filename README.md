# Kosmorrolib - a library to compute your ephemerides!
[![Coverage Status](https://coveralls.io/repos/github/Deuchnord/kosmorro/badge.svg)](https://coveralls.io/github/Deuchnord/kosmorro) [![Version on PyPI](https://img.shields.io/pypi/v/kosmorro)](https://pypi.org/project/kosmorro) [![Discord](https://img.shields.io/discord/650237632533757965?logo=discord&label=%23kosmorro)](https://discord.gg/nyemBqE)

## Installation

### Requirements

Kosmorro requires the following software to work:

- Python ≥ 3.5.0
- PIP

### Production environment

Keep in mind that Kosmorro is still in alpha development stage and is not considered as stable.

#### Linux

##### Arch Linux, Manjaro…

Kosmorro is available [in the AUR](https://aur.archlinux.org/packages/kosmorro).

##### Other distributions

Kosmorro is available [on PyPI](https://pypi.org/project/kosmorro/), a repository dedicated to Python.
First, install `python-pip` on your system and invoke the following command: `pip install kosmorro`.

#### macOS

Currently, macOS does not provide Python 3, so you will first have to install it.
If you don't have it, first install [HomeBrew](https://formulae.brew.sh), then install Python 3: `brew install python`.

This will install Python 3 and its PIP on your system. Note that their executables are called `python3` and `pip3`.
Now, you can install Kosmorro with your PIP: `pip3 install kosmorro`.

#### Windows

Kosmorro being at an early-stage development, Windows is not supported officially for now.

### Development environment

First, install [Pipenv](https://pypi.org/project/pipenv/).

Clone this repository and run `pipenv sync` to install all the dependencies.
Then, run Kosmorro by invoking `pipenv run python kosmorro`.

For comfort, you may want to invoke `pipenv shell` first and then just `python kosmoro`.

## Using Kosmorro

Using Kosmorro is as simple as invoking `kosmorro` in your terminal!

By default, it will give you the current Moon phase and, if any, the events that will occur today.
To get the rise, culmination and set of the objects of the Solar system, you will need to give it your position on Earth: get your current coordinates (with [OpenStreetMap](https://www.openstreetmap.org) for instance), and give them to Kosmorro by invoking it with the following parameters: `--latitude=X --longitude=Y` (replace `X` by the latitude and `Y` by the longitude).

Kosmorro has a lot of available options. To get a list of them, run `kosmorro --help`, or read its manual with `man kosmorro`.

Note: the first time it runs, Kosmorro will download some important files needed to make the computations. They are stored in a cache folder named `.kosmorro-cache` located in your home directory (`/home/<username>` on Linux, `/Users/<username>` on macOS).

### Exporting to PDF

Kosmorro can export the computation results to PDF files, but this feature requires first that you install some additional dependencies. Before you use this feature, please check these packages are installed:

- **A LaTeX distribution:**
    - Linux: install TeXLive through your packages manager. Kosmorro just needs the minimal installation, you don't need any extension.
    - macOS: install [MacTeX](https://www.tug.org/mactex/), the basic version will suffice:
        - from the official website, choose the _smaller download_
        - with Brew: `brew install basictex`
- **The `latex` Python library:**
    - Arch Linux: the library is available [on the AUR](https://aur.archlinux.org/packages/python-latex)
    - Any other systems: install it through PyPI: `pip install latex`

These dependencies are not installed by default, because they take a lot of place and are not necessary if you are not interested in generating PDF files.
The first time you ask Kosmorro to create a PDF, it may be a little verbose. You can ignore its blahblah.

### Opening the GUI

![Screenshot](.github/assets/gui-screenshot.png)

Kosmorro provides a graphical user interface that can be easily launched by invoking the `kosmorro --gui` command.

To run it, you will have to install the `wxpython` package:

- **On Linux**, wxPython is most likely provided by your packages manager.
- **On Mac**, install wxPython by invoking `pip3 install wxPython`.

  Alternatively, you may download the DMG file on the release page (note that you won't be able to use the command
  line in this case).
