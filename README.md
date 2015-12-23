Django Tastypie Batch
=====================

Adds a batch request endpoint to tastypie `Api`'s.

Install
-------

Install from git using pip:

```bash
pip install -e git+https://github.com/jonykalavera/django-tastypie-batch.git#egg=django-tastypie-batch
```

Add `tastypie_batch` to your `INSTALLED_APPS`.


Usage guide
-----------

Use the custom `BatchApi` instead of tastypie's `Api` class,

```python
from batch.api import BatchApi

v1_api = BatchApi(api_name='v1')
```

or the namespaced version.

```python
from batch.api import NamespacedBatchApi

v1_api = NamespacedBatchApi(api_name='v1', urlconf_namespace='ns')
```

Alternatively, you can use the provided mixin to add to your own custom `Api`.

```python
from batch.api import BatchEndpointMixin
from tastypie.api import Api


class CustomApi(BatchEndpointMixin, Api):
    """
    Custom tastypie Api
    """
    # ...
```

Making batch requests
---------------------

a list of request descriptors must be posted to the ```batch``` endpoint.
```json
[
    {
        "path": "/api/v1/foo/",
        "params": {
            "limit": 1
        }
    },
    {
        "path": "/api/v1/bar/",
        "params": {
            "limit": 1
        }
    }
]
```

server will answer with a list of responses for the requested endpoints.

```json
[
  {
    "body": "{\"meta\": {\"limit\": 1, \"next\": \"/api/v1/foo/?limit=1&offset=1\", \"offset\": 0, \"previous\": null, \"total_count\": 2}, \"objects\": [{\"id\": 1, \"name\": \"hello\", \"resource_uri\": \"/api/v1/foo/1/\"}]}",
    "cookies": {},
    "headers": {
      "cache-control": [
        "Cache-Control",
        "no-cache"
      ],
      "content-type": [
        "Content-Type",
        "application/json"
      ],
      "vary": [
        "Vary",
        "Accept"
      ],
      "x-frame-options": [
        "X-Frame-Options",
        "SAMEORIGIN"
      ]
    },
    "params": {
      "limit": 1
    },
    "path": "/api/v1/foo/",
    "status": 200
  },
  {
    "body": "{\"meta\": {\"limit\": 1, \"next\": \"/api/v1/bar/?limit=1&offset=1\", \"offset\": 0, \"previous\": null, \"total_count\": 2}, \"objects\": [{\"id\": 1, \"name\": \"hello\", \"resource_uri\": \"/api/v1/bar/1/\"}]}",
    "cookies": {},
    "headers": {
      "cache-control": [
        "Cache-Control",
        "no-cache"
      ],
      "content-type": [
        "Content-Type",
        "application/json"
      ],
      "vary": [
        "Vary",
        "Accept"
      ],
      "x-frame-options": [
        "X-Frame-Options",
        "SAMEORIGIN"
      ]
    },
    "params": {
      "limit": 1
    },
    "path": "/api/v1/bar/",
    "status": 200
  }
]
```


ToDo's
------
* test cases.
* POST, PUT, PATCH, DELETE ¿?
* test other authentication methods.
* test other serialization methods besides json.
