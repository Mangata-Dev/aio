from aiohttp import web
import yaml
from datetime import datetime

async def _tick_(request):
    try:
        # 0 : extract payload dict
        json = await request.json()

        try:
            with open(f'./tick/data/'+datetime.now().isoformat()+'.yml', 'w') as yml_file:
                documents = yaml.dump(json, yml_file)
        except Exception as expYalm :
            return web.json_response({'err': {'str': str(expYalm), 'typ': str(type(expYalm))}}, status=500)

        return web.json_response(dict(json=json))

    # $>
    except Exception as exp:
        # <!
        # !0 return what's wrong in string and the type of the exception should be enough to understand where you're wrong noobs
        return web.json_response({'err': {'str': str(exp), 'typ': str(type(exp))}}, status=500)
# `< - - - - - - - - - - - -
