import asyncio
import websockets
from datetime import datetime
from ocpp.routing import on, after
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result, call
import logging

#from pyfirmata import OUTPUT

from ocpp.v20 import ChargePoint as cp
from ocpp.v201.call import SetNetworkProfilePayload
from ocpp.v16.datatypes import MeterValue

logging.basicConfig(level=logging.DEBUG)


class ChargePoint(cp):

    @on(Action.BootNotification)
    def on_boot_notitication(self, charge_point_vendor, charge_point_model, **kwargs):
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )





    @on(Action.Heartbeat)
    def on_heartbeat(self):
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().isoformat(),
        )

    @after(Action.Heartbeat)
    async def update_heartbeat_interval(self):
        request = call.ChangeConfigurationPayload(
            key="HeartbeatInterval",
            value="123"
        )
        response = await self.call(request)
        # do something with the response...(code never reached)
        print(response)


async def on_connect(websocket, path):
    """ For every new charge point that connects, create a ChargePoint instance
    and start listening for messages.

    """
    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)
    print("charging point", cp)
    await cp.start()


def digitalWrite(param, HIGH):
    pass


def pinMode(param, OUTPUT):
    pass


async def main(HIGH=None):
    server = await websockets.serve(
        on_connect,
        '192.168.105.92',
        5000,
        subprotocols=['ocpp1.6']
    )

    await server.wait_closed()
    pinMode(17, OUTPUT);
    digitalWrite(17, HIGH);


if __name__ == '__main__':
    asyncio.run(main())