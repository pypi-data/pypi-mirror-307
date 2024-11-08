# paperqa-api

Python client for interacting with paperqa app

# Usage

Make sure to set the environment variable `PQA_API_KEY` to your API token.

```sh
export PQA_API_TOKEN=pqa-...
```

To query agent:

```py
import pqapi
response = pqapi.agent_query(
    "Are COVID-19 vaccines effective?"
)
```

you can do it with async too:

```py
import pqapi
response = await async_agent_query(query, "default")
```

The response object contains information about the sources, cost, and other details. To get just the answer:

```py
print(response.answer)
```

# Development

If developing, you can change the server URL endpoint to a local PQA server with

```sh
export PQA_URL="http://localhost:8080"
```
