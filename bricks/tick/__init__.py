# 
from tick.src.tick import (
  _tick_,
  _plot_symbol_
)

#
from aiohttp import web

#
app_tick = web.Application()

#
app_tick.add_routes([

  web.post('/',   _tick_),
  web.get('/{symbol}',   _plot_symbol_)

])
