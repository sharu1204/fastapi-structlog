# fastapi-structlog

Capturing HTTP requests with pretty format (JSON) in [FastAPI framework](https://fastapi.tiangolo.com/) (w/uvicorn,gunicorn) with [Structlog](https://www.structlog.org/en/stable/).

## How to Run FastAPI with Structlog

Simply running `docker-compose` command

```sh
docker-compose up
```

and FastAPI with Structlog will run in our local.

## Example of Logging Outputs

When we access [http://127.0.0.1:8000/ping](http://127.0.0.1:8000/ping), our local FastAPI container shows logging outputs like below:

```json
{
  "cookies": { "_ga": "GA1.1.1766553845.1593588583" },
  "event": "processed a request",
  "level": "info",
  "logger": "uvicorn.access",
  "process_time": 0.002379179000854492,
  "request_id": "0233445c-8ea8-4f82-990d-e29665bd92e2",
  "scope": {
    "app": "<fastapi.applications.FastAPI object at 0x7f96ff48e160>",
    "client": ["172.24.0.1", 51612],
    "endpoint": "<function ping at 0x7f96fe115c10>",
    "fastapi_astack": "<contextlib.AsyncExitStack object at 0x7f96fde8dfd0>",
    "headers": [
      ["host", "localhost"],
      ["connection", "keep-alive"],
      ["cache-control", "max-age=0"],
      ["upgrade-insecure-requests", "1"],
      [
        "user-agent",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
      ],
      [
        "accept",
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
      ],
      ["sec-fetch-site", "none"],
      ["sec-fetch-mode", "navigate"],
      ["sec-fetch-user", "?1"],
      ["sec-fetch-dest", "document"],
      ["accept-encoding", "gzip, deflate, br"],
      ["accept-language", "en-US,en;q=0.9"],
      ["cookie", "_ga=GA1.1.1766553845.1593588583"]
    ],
    "http_version": "1.1",
    "method": "GET",
    "path": "/ping",
    "path_params": {},
    "query_string": "",
    "raw_path": "/ping",
    "root_path": "",
    "router": "<fastapi.routing.APIRouter object at 0x7f96ff1a95e0>",
    "scheme": "http",
    "server": ["172.24.0.2", 80],
    "type": "http"
  },
  "status_code": 200,
  "timestamp": "2020-08-31T00:06:04.240352Z",
  "url": "http://localhost/ping"
}
```

## How to Capture HTTP Requests with Structlog

As you can see in [main.py](./app/main.py), there are some configurations needed to capture HTTP requests with Structlog.

- [Set structlog to enable JsonRenderer with rapidjson](./app/main.py#L20-L31)
- [Utilize FastAPI middleware to bind structlog's threadlocal](./app/main.py#L34-L56)
- [Clear guvicorn access log to omit original HTTP request logging](./app/main.py#L18)

## Structlog vs python-json-logger

We can also utilize [python-json-logger](https://github.com/madzak/python-json-logger) to simply capture HTTP requests with JSON format in FastAPI.

- Sample [main.py](https://gist.github.com/sharu1204/db9781f61d791645b7dfb5cf8cb875a2)

<details><summary>Logging Outputs with python-json-logger</summary><div>

```json
{
  "message": "172.24.0.1:51812 - \"GET /ping HTTP/1.1\" 200",
  "status_code": 200,
  "scope": {
    "type": "http",
    "http_version": "1.1",
    "server": ["172.24.0.2", 80],
    "client": ["172.24.0.1", 51812],
    "scheme": "http",
    "method": "GET",
    "root_path": "",
    "path": "/ping",
    "raw_path": "b'/ping'",
    "query_string": "b''",
    "headers": [
      ["b'host'", "b'localhost'"],
      ["b'connection'", "b'keep-alive'"],
      ["b'cache-control'", "b'max-age=0'"],
      ["b'upgrade-insecure-requests'", "b'1'"],
      [
        "b'user-agent'",
        "b'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'"
      ],
      [
        "b'accept'",
        "b'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'"
      ],
      ["b'sec-fetch-site'", "b'none'"],
      ["b'sec-fetch-mode'", "b'navigate'"],
      ["b'sec-fetch-user'", "b'?1'"],
      ["b'sec-fetch-dest'", "b'document'"],
      ["b'accept-encoding'", "b'gzip, deflate, br'"],
      ["b'accept-language'", "b'en-US,en;q=0.9'"],
      ["b'cookie'", "b'_ga=GA1.1.1766553845.1593588583'"]
    ],
    "fastapi_astack": "<contextlib.AsyncExitStack object at 0x7f0af5e78790>",
    "app": "<fastapi.applications.FastAPI object at 0x7f0af6cf4730>",
    "router": "<fastapi.routing.APIRouter object at 0x7f0af6cf42b0>",
    "endpoint": "<function ping at 0x7f0af5f54d30>",
    "path_params": {}
  }
}
```

</div></details>

However, if we want customized logging outputs as we want (e.g. add uuid to each request or omit unnecessary key-value), structlog has an advantage. Performance-wise, `python-json-logger` is slightly faster than Structlog in small number of requests (100 requests/second), but both of them have a similar performance over 1000 requests/second.
