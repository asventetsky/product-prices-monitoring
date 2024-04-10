# Lambda: historic prices provider
> Provides prices for a specified period (`from` - `to`).

## Developing

### Running locally

```shell
cd backend/historic_prices_provider/misc
```

```shell
docker compose up
```

```shell
httpie :9000/2015-03-31/functions/function/invocations queryStringParameters[productId]=20000008040938 queryStringParameters[from]=2024-03-26 queryStringParameters[to]=2024-03-28
```