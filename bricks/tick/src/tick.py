import aiohttp
from aiohttp import web
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import pandas as pd
import matplotlib.pyplot as plt


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
        if request.body_exists:
            param1 = await request.json()
        else:
            return web.json_response({'err': {'str': 'Bad request body'}}, status=400)

        transport = AIOHTTPTransport(url="https://dbschool.alcyone.life/graphql")
        listofdf = []
        for symbol in param1['symbol']:

            # Create a GraphQL client using the defined transport
            async with Client(
                    transport=transport, fetch_schema_from_transport=True,
            ) as client:
                query = gql(
                    """
                      query {
                        tickers(where: { symbol: "%s" }) {
                            price
                            created_at
                        }
                        }  
                    """ % symbol
                )

            # Execute the query on the transport
                result = await client.execute(query)
                history_price = result['tickers']
                history_price_df = pd.DataFrame.from_dict(history_price)
                history_price_df = history_price_df.rename({'price': symbol}, axis=1)
                listofdf.append(history_price_df)

        dfs = [df.set_index('created_at') for df in listofdf]
        histpriceconcat = pd.concat(dfs, axis=1)
        for i, col in enumerate(histpriceconcat.columns):
            histpriceconcat[col].plot()

        plt.title('Price Evolution Comparison')

        plt.xticks(rotation=70)
        plt.legend(histpriceconcat.columns)

        # Saving the graph into a JPG file
        plt.savefig(f'./tick/plots/symbols_price_curve.png', bbox_inches='tight')
        return aiohttp.web.FileResponse(f'./tick/plots/symbols_price_curve.png')
    except Exception as exp:
        # <! !0 return what's wrong in string and the type of the exception should be enough to understand where
        # you're wrong noobs
        return web.json_response({'err': {'str': str(exp), 'typ': str(type(exp))}}, status=500)

