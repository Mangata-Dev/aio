# 
from tick.src.tick import (
  _tick_
)

#
from aiohttp import web

#
app_tick = web.Application()

#
app_tick.add_routes([

  web.post('/',   _tick_),
  
])
