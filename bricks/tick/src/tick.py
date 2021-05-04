import aiohttp
from aiohttp import web
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


async def _tick_(request):
    try:
        # 0 : extract payload dict
        # json = await request.json()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://51.15.17.205:9000/tick/Tony') as response:
                json = await response.json()

        transport = AIOHTTPTransport(url="https://dbschool.alcyone.life/graphql")

        # Create a GraphQL client using the defined transport
        async with Client(
                transport=transport, fetch_schema_from_transport=True,
        ) as client:
            data = json['data']
            for tick in data:
                query = gql(
                    """
                        mutation {
                            createTicker(input: { data:{ symbol: "%s", price: %.2f } }) {
                                ticker {
                                    symbol
                                    price
                                }
                            }
                        }
                    """ % (str(tick['symbol']), float(tick['price']))
                )

                # Execute the query on the transport
                result = await client.execute(query)
                print(result)

        return web.json_response(dict(json=json))

    # $>
    except Exception as exp:
        # <! !0 return what's wrong in string and the type of the exception should be enough to understand where
        # you're wrong noobs
        return web.json_response({'err': {'str': str(exp), 'typ': str(type(exp))}}, status=500)


async def _plot_symbol_(request):
    try:
        # name = request.match_info.get('symbol', "Anonymous")
        param1 = request.rel_url.query.get('symbol', "Anonymous")
        transport = AIOHTTPTransport(url="https://dbschool.alcyone.life/graphql")

        # Create a GraphQL client using the defined transport
        async with Client(
                transport=transport, fetch_schema_from_transport=True,
        ) as client:
            query = gql(
                """
                  query {
                    tickers(where: { symbol_contains: "%s" }) {
                        symbol
                        price
                        created_at
                    }
                    }   
                """ % param1
            )

            # Execute the query on the transport
            result = await client.execute(query)
        return web.json_response(result)
    except Exception as exp:
        # <! !0 return what's wrong in string and the type of the exception should be enough to understand where
        # you're wrong noobs
        return web.json_response({'err': {'str': str(exp), 'typ': str(type(exp))}}, status=500)

