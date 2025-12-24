#!/usr/bin/env python3

import asyncio
from mavsdk import System
from mavsdk.action import ActionError

async def run():
    drone = System()

    print("Waiting for drone to connect ...")
    await drone.connect(system_address="udpin://0.0.0.0:14540") # receiving data from any interface (sitl on same computer, telemetry over wifi , simulation running on a different lap)
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to drone")
            break
    
    async for health in drone.telemetry.health(): # asynchronous generator (async for) is used to subscribe
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimaion OK")
            break

    print("-- Arming")
    try:
        await drone.action.arm()
    except ActionError as e:
        print(f"Arming failed : {e}")
        return
    
    target_altitude = 10.0
    print(f"-- Setting takeoff altitude to {target_altitude}m")
    await drone.action.set_takeoff_altitude(target_altitude)

    print("-- Starting Takeoff")
    await drone.action.takeoff()

    print(f"-- Monitoring altitude until {target_altitude}m is reached")
    async for position in drone.telemetry.position():
        relative_alt = position.relative_altitude_m
        print(f"Reached : {relative_alt:.2f} / {target_altitude}m",end='\r')

        if abs(relative_alt - target_altitude) < 0.3 :
            print(f"-- Target altitude {target_altitude}m is reached")
            break

    print("-- Going to preseted location")
    await drone.action.goto_location(47.398036222362471, 8.5450146439425509, 10.0,0.0)
    await asyncio.sleep(5.0)

    print("-- Holding position for 5 seconds")
    await drone.action.hold()
    await asyncio.sleep(5.0)



    print("-- Initiating RTL")
    await drone.action.set_return_to_launch_altitude(20.0) # this action specific for PX-4, does'nt work with ardupilot 
    await drone.action.return_to_launch()
    async for is_in_air in drone.telemetry.in_air():
        if not is_in_air:
            print("-- Landed succefully (Disarmed by RTL)")
            break 


if __name__ == "__main__":

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("Script cancelled by the user")   