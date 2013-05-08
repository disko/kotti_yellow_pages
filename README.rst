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

Included Javascript Libraries
-----------------------------

``kotti_yellow_pages`` makes heavy use of third party Javascript libraries.

These libraries are bundled with this package:

    -   AngularJS
        (http://angularjs.org/)

        The reason why AngularJS is bundled instead of using the existing
        ``js.angular`` fanstatic package is, that we have to make sure that
        AngularJS uses jQuery and not its included ``jQuery lite``.  Therefore
        the Fanstatic resource has to declare a dependency on
        ``js.jquery.jquery``, which ``js.angular`` doesn't provide (and is right
        with not doing so).

    -   AngularUI
        (http://angular-ui.github.io/)

        Same reason as above.

    -   UI Bootstrap
        (http://angular-ui.github.io/bootstrap/)

        Same reason as above.

    -   Leaflet awesome markers
        (https://github.com/lvoogdt/Leaflet.awesome-markers)

        Should be in its own ``js.leaflet_awesome_markers`` package instead, or
        probably part of ``js.leaflet``.


.. _Kotti: http://pypi.python.org/pypi/Kotti
