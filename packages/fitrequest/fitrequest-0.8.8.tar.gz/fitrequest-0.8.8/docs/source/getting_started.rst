Getting started
===============

Installation
------------

Before using the ``FitRequest``, you need to install it:

.. code-block:: bash

    pip install --upgrade fitrequest

How to use it
-------------

You can implement FitRequest to create your own client class like so:

.. code-block:: python

    from fitrequest.client import FitRequest


    class RestApiClient(FitRequest):
        base_url = "http://base_api_url"
        base_client_name="rest_api"
        _docstring_template = 'GET request on endpoint: {endpoint}\nDocs URL anchor: http://base_api_url/docs/{docs_url_anchor}'
        _methods_binding = [
            {
                'name': 'get_item',
                'endpoint': '/items/{}',
                'docs_url_anchor': 'items/items_list',
                'resource_name': 'item_id',
            }
        ]


More examples are coming in the future.
