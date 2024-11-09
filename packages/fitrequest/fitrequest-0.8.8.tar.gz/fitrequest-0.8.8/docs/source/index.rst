Welcome to FitRequest
=====================

Useful Links
------------

* **Code**: `fitrequest GitLab <https://gitlab.com/public-corner/fitrequest/>`_
* **Pypi**: `fitrequest PyPI <https://pypi.org/project/fitrequest/>`_

Overview
--------

``FitRequest`` is a Python class designed to ease client for REST API. It will generate dynamically methods based on a dict attribute named `_methods_binding`.
It allows you to have a template docstring for all your methods and also create a save method to dump the data retrieved to a file instead of returning the value.

In the future we will add more authentication methods and HTTP methods (only GET is supported as of now).

Contents
--------

.. toctree::
   :maxdepth: 2

   getting_started
   fitrequest
   method_details
   methods_generator
