==================
kotti_yellow_pages
==================

Yellow Pages content type for `Kotti`_.

THIS IS VERY MUCH WORK IN PROGRESS.  DO NOT USE IT FOR ANYTHING BUT
DEVELOPMENT!  THINGS WILL CHANGE RAPIDLY, API IS IN NO WAY STABLE YET!

Setup
=====

To activate the ``kotti_yellow_pages`` add-on in your Kotti site, you need to
add an entry to the ``kotti.configurators`` setting in your Paste
Deploy config.  If you don't have a ``kotti.configurators`` option,
add one.  The line in your ``[app:main]`` (or ``[app:kotti]``, depending on how
you setup Fanstatic) section could then look like this::

    kotti.configurators = kotti_yellow_pages.kotti_configure

https://github.com/leaflet-extras/leaflet.css
http://tombatossals.github.io/angular-leaflet-directive/

.. _Kotti: http://pypi.python.org/pypi/Kotti
