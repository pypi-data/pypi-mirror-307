# Yandex Go for Business SDK (Python)

---

Officially supported Python client for Yandex Go for Business

---

**Documentation**: <a href="https://taxi__business-api.docs-viewer.yandex.ru/ru/" target="_blank">https://taxi__business-api.docs-viewer.yandex.ru/ru/

---

## Quickstart

### Prerequisites

- Python 3.8 or higher
- `pip` version 9.0.1 or higher

If necessary, upgrade your version of `pip`:

```sh
$ python -m pip install --upgrade pip
```

If you cannot upgrade `pip` due to a system-owned installation, you can
run the example in a virtualenv:

```sh
$ python -m pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ python -m pip install --upgrade pip
```

Install Yandex Go for Business SDK:

```sh
$ python -m pip install yandex_b2b_go
```

## Getting started

Your requests are authorized via an OAuth token.

```python
client = yandex_b2b_go.Client(token='y2_...')
```

Or you can use context manager
```python
async with yandex_b2b_go.Client(token='y2_...') as client:
    pass
```

---

## Get user list

Example method for get users list.
```python
import yandex_b2b_go

TOKEN = 'y2_...'
client = yandex_b2b_go.Client(token=TOKEN)
user_manager = yandex_b2b_go.UserManager(client=client)
users = await user_manager.list(limit=20, cursor='djEgMTY2M...MGM3OTE=')
```

This method return class `UserListResponse`

---

## Get user create

Example method for user create.
```python
import yandex_b2b_go

TOKEN = 'y2_...'
client = yandex_b2b_go.Client(token=TOKEN)
user_manager = yandex_b2b_go.UserManager(client=client)
user = yandex_b2b_go.typing.User(
    fullname='Иванов Илья',
    phone='+79990000000',
    is_active=True,
)
response = await user_manager.create(user=user)
```

This method return class `UserCreateResponse`

---

## Class Client have parameters
- `timeout` - the time in seconds to limit the execution of the request
- `log_level` - the logging level for a specific method. Default `logging.INFO`
- `log_request` - whether to log the entire request. Default `False`
- `log_response` - whether to log the entire response. Default `False`

## Example

Set `log_level = WARNING` and `log_request = True`

```python
import logging
import yandex_b2b_go

TOKEN = 'y2_...'
client = yandex_b2b_go.Client(token=TOKEN, log_level=logging.WARNING, log_request=True)
user_manager = yandex_b2b_go.UserManager(client=client)
users = await user_manager.list(limit=1)
```
Output:
```commandline
2024-09-17 16:20:03,166 WARNING Request=GET, for url=https://b2b-api.go.yandex.ru/integration/2.0/users?limit=1, params={'limit': '1'}, body=None
2024-09-17 16:20:03,814 WARNING GET request https://b2b-api.go.yandex.ru/integration/2.0/users success with status code 200
```

---

Set `log_response = True`
```python
import yandex_b2b_go

TOKEN = 'y2_...'
client = yandex_b2b_go.Client(token=TOKEN, log_response=True)
user_manager = yandex_b2b_go.UserManager(client=client)
users = await user_manager.list(limit=1)
```
Output:
```commandline
2024-09-17 16:22:22,995 INFO Performing GET request to https://b2b-api.go.yandex.ru/integration/2.0/users
2024-09-17 16:22:23,276 INFO GET request https://b2b-api.go.yandex.ru/integration/2.0/users success with status code 200, body={'items': [{'fullname': 'Иванов Илья', 'is_active': True, 'phone': '+79990000000', 'id': '0516587…..c5a8adb58', 'is_deleted': False, 'cost_center': '', 'department_id': '9080a2……208a1856', 'email': 'email1@email.ru', 'limits': [{'limit_id': 'e31cc52437...', 'service': 'eats2'}, {'limit_id': '4afef98...', 'service': 'drive'}, {'limit_id': '20569bb9d...', 'service': 'taxi'}], 'nickname': 'id1234572', 'client_id': '1f300a6…..edf867021c'}], 'limit': 1, 'total_amount': 20, 'next_cursor': 'djEgMTY2NjA3OTAN….GM4MTgwMDFlNTAzYjg3NTQ='}
```

---
## Contributing
### Dependencies
Use `make deps` command to install library, its production and development dependencies.

### Formatting
Use `make format` to autoformat code with black tool.

### Tests
- `make test` to run tests for current python version
- `make lint` to run only linters for current python version
