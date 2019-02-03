InSight Raw Media Images
========================

|Build| |Coverage|

.. |Build| image:: https://img.shields.io/travis/seignovert/python-insight-images.svg?label=CI&logo=travis-ci&logoColor=white
        :target: https://travis-ci.org/seignovert/python-insight-images
.. |Coverage| image:: https://coveralls.io/repos/github/seignovert/python-insight-images/badge.svg?branch=master
        :target: https://coveralls.io/github/seignovert/python-insight-images?branch=master

Python package to list and download all original images from
`InSight <https://mars.nasa.gov/insight/multimedia/raw-images/>`_.

|InSight|

.. |InSight| image:: catch.gif
        :target: https://mars.nasa.gov/raw_images/1801/

Install
-------
With the ``source files``:

.. code:: bash

    $ git clone https://github.com/seignovert/python-insight-images insight ; cd insight ; python setup.py install

Python usage
------------
Query InSight latest images:

.. code:: python

    >>> from insight import API

    >>> API.count_imgs()
    732

    >>> imgs = API.get_images(10)
    [<InSight Image> D000M0066_602399124EDR_F0000_0250M_,
    ...
    <InSight Image> C000M0066_602378643EDR_F0000_2707M_]

    >>> imgs[0].download(out='insight.png')
    Download insight.png: 1260 kB [00:00, 3583.31 kB/s]

    >>> API.sync()
    70%|█████████▌   | 516/732 [06:47<02:37,  1.37it/s]

CLI usage
---------
Download all images:

.. code:: bash

    $ insight-sync --help
    usage: insight-sync [-h] [--overwrite]

    Sync InSight Raw Media Images

    optional arguments:
      -h, --help       show this help message and exit
      --overwrite, -o  Re-download all

    $ insight-sync
    70%|█████████▌   | 516/732 [06:47<02:37,  1.37it/s]


Disclaimer
----------
This project is not supported or endorsed by either JPL or NASA.
The code is provided "as is", use at your own risk.
