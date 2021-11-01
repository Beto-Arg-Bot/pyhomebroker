from pyhomebroker import HomeBroker
import asyncio

dni='41562055'
user='bautistab'
passw='taw9YFX!wrf1rpu@fnf'
brokerId=12

async def test():
    broker=HomeBroker(brokerId)
    await broker.auth.login(dni=dni,user=user,password=passw,raise_exception=True)
    settlement=broker.online.get_settlement_for_request('spot')
    response=await broker.online._scrapping.get_asset('ggal',settlement)
    responseString=str(response)
    responseString=responseString.replace("'",'"')
    responseString=responseString.replace("None",'null')
    responseString=responseString.replace("True",'true')
    responseString=responseString.replace("False",'false')
    print(responseString)

loop=asyncio.get_event_loop()
loop.run_until_complete(test())
