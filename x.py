from pyhomebroker import HomeBroker
import asyncio

dni='41562055'
user='bautistab'
passw='taw9YFX!wrf1rpu@fnf'
brokerId=12

async def test():
    broker=HomeBroker(brokerId)
    cookies=await broker.auth.login(dni=dni,user=user,password=passw,raise_exception=True)
    # response=broker.online._scrapping.get_asset('ggal','')
    # print(response)
    print(type(cookies))
    print(cookies)

loop=asyncio.get_event_loop()
loop.run_until_complete(test())
