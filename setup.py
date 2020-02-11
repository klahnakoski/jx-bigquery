# encoding: utf-8
# THIS FILE IS AUTOGENERATED!
from __future__ import unicode_literals
from setuptools import setup
setup(
    author='Kyle Lahnakoski',
    author_email='kyle@lahnakoski.com',
    classifiers=["Development Status :: 4 - Beta","Topic :: Software Development :: Libraries","Topic :: Software Development :: Libraries :: Python Modules","License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)","Programming Language :: Python :: 2.7","Programming Language :: Python :: 3.6","Programming Language :: Python :: 3.7","Programming Language :: Python :: 3.8"],
    description='jx-bigquery - JSON Expressions for BigQuery',
    include_package_data=True,
    install_requires=["google-cloud-bigquery","jx-python>=3.47.20042","jx-python>=3.47.20042","mo-dots>=3.47.20042","mo-future>=3.47.20042","mo-json>=3.47.20042","mo-kwargs>=3.47.20042","mo-logs>=3.47.20042","mo-sql>=3.47.20042","mo-times>=3.46.20032","mo-times>=3.46.20032"],
    license='MPL 2.0',
    long_description='# jx-bigquery\nJSON Expressions for BigQuery\n\n\n## Configuration\n\n```json\n{\n    "table": "my_table_name",\n    "top_level_fields": {},\n    "partition": {\n        "field": "submit_time",\n        "expire": "2year"\n    },\n    "id": {\n        "field": "id",\n        "version": "last_modified"\n    },\n    "cluster": [\n        "id",\n        "last_modified"\n    ],\n    "schema": {\n        "id": "integer",\n        "submit_time": "time",\n        "last_modified": "time"\n    },\n    "sharded": true,\n    "account_info": {\n        "private_key_id": {\n            "$ref": "env://BIGQUERY_PRIVATE_KEY_ID"\n        },\n        "private_key": {\n            "$ref": "env://BIGQUERY_PRIVATE_KEY"\n        },\n        "type": "service_account",\n        "project_id": "my-project-id",\n        "client_email": "me@my_project.iam.gserviceaccount.com",\n        "client_id": "12345",\n        "auth_uri": "https://accounts.google.com/o/oauth2/auth",\n        "token_uri": "https://oauth2.googleapis.com/token",\n        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",\n        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test-treeherder-extract%40moz-fx-dev-ekyle-treeherder.iam.gserviceaccount.com"\n    }\n}\n```\n\n\n* `table` - Any name you wish to give to this table, the \n* `top_level_fields` - Map from \n* `partition` - \n        "field": "submit_time",\n        "expire": "2year"\n    },\n* `id` - \n        "field": "id",\n        "version": "last_modified"\n    },\n* `cluster` - \n        "id",\n        "last_modified"\n    ],\n* `schema` - \n        "id": "integer",\n        "submit_time": "time",\n        "last_modified": "time"\n    },\n* `sharded": true` - \n* `account_info` - The content of the application  \n\n\n\n\n\n\n## Usage\n\nSetup `Dataset` with an applicaiotn name\n\n```python\n    destination = bigquery.Dataset(\n        dataset=application_name, \n        kwargs=settings\n    ).get_or_create_table(settings.destination)\n```\n\n\n\n\n```python\n    destination.extend(documents)\n```\n\n',
    long_description_content_type='text/markdown',
    name='jx-bigquery',
    packages=["jx_bigquery/expressions","jx_bigquery"],
    url='https://github.com/klahnakoski/jx-bigquery',
    version='3.47.20042'
)