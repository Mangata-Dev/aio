import aiohttp
import asyncio
from rich import print
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


async def main():

    async with aiohttp.ClientSession() as session:
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url="https://dbschool.alcyone.life/graphql")

        async with session.get('http://51.15.17.205:9000/tick/Tony') as response:
            json = await response.json()

        # Create a GraphQL client using the defined transport
        async with Client(
                transport=transport, fetch_schema_from_transport=True,
        ) as client:
            data = json['data']
            for tick in data:

                query = gql(
                    """
                        mutation {
                            createTicker(input: { data:{ symbol: "%s", price: %d } }) {
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

loop = asyncio.get_event_loop()
loop.run_until_complete(main())