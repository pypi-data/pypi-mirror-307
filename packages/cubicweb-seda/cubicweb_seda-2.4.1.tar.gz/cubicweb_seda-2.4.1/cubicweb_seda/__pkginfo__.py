# pylint: disable=W0622
"""cubicweb-seda application packaging information"""

modname = "seda"
distname = "cubicweb-seda"

numversion = (2, 4, 1)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "Data Exchange Standard for Archival"
web = f"https://forge.extranet.logilab.fr/cubicweb/cubes/{distname}"

__depends__ = {
    "cubicweb[postgresql]": ">=4.0.0, < 5.0",
    "cubicweb-web": ">= 1.1.0, < 2.0.0",
    "cubicweb-eac": "== 0.10.0",
    "cubicweb-skos": ">= 3.1.0",
    "cubicweb-compound": ">= 1.0.0",
    "cubicweb-relationwidget": ">= 0.10",
    "cubicweb-squareui": ">= 2.0",
    "cubicweb-geocoding": ">= 1.0",
    "pyxst": ">= 0.3.2",
    "rdflib": ">= 4.1",
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]
