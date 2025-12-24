#!/usr/bin/env python3

import asyncio
from mavsdk import System
from mavsdk.action import ActionError
# from mavsdk.offboard import OffboardError
# from mavsdk.offboard import PositionNedYaw

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
    
    # print("-- Setting initial setpoint")
    # # Usage: PositionNedYaw(north_m, east_m, down_m, yaw_deg)
    # # WARNING: 'down' is positive. 0.0 is the ground. -5.0 is 5m altitude.
    # target_pos = PositionNedYaw(0.0, 0.0, -5.0, 0.0)
    # await drone.offboard.set_position_ned(target_pos) #Set the position in NED coordinates and yaw
    
    # try:
    #     await drone.offboard.start()
    # except OffboardError as error:
    #     print(f"-- Starting offboard moade failed : {error._result.result}")
    #     print("-- Disarming")
    #     await drone.action.disarm()
    #     return


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
    async for height in drone.telemetry.position():
        relative_alt = height.relative_altitude_m
        print(f"Reached : {relative_alt:.2f} / {target_altitude}m",end='\r')

        if abs(relative_alt - target_altitude) < 0.3 :
            print(f"-- Target altitude {target_altitude}m is reached")
            break


    # for getting absolute altitude (AMSL) to calculate target AMSL
    # Need this need because 'go_to_location' uses AMSL, not relative height
    async for postn_ in drone.telemetry.position():
        current_amsl = postn_.absolute_altitude_m
        target_amsl = current_amsl + 0.0
        break

    print("-- Going to preseted location")
    target_latitude = -35.36326176 #35.36326176 149.16530170
    target_longitude = 149.16530170
    target_yaw = 0.0
    await drone.action.goto_location(target_latitude, target_longitude, target_amsl, target_yaw) # latitude_deg, longitude_deg, absolute_altitude_m, yaw_deg
    async for postn in drone.telemetry.position():
        current_latitude = postn.latitude_deg
        current_longitude = postn.longitude_deg
        current_relative_altitude = postn.relative_altitude_m
        print(f"Present position (lat, long, rel_alt) = ({current_latitude:.2f}, {current_longitude:.2f}, {current_relative_altitude})",end='\r')
        await asyncio.sleep(0.1)

        if abs(target_latitude - current_latitude) < 0.01 and abs(target_longitude - current_longitude) < 0.01:
            print("-- Reached preseted location")
            break

    await asyncio.sleep(5.0)

    #print("-- Holding position for 5 seconds")
    # await drone.action.hold()

    '''
    Question  I noted that await drone.action.hold() is causing to changing mode to LOITER thereby hitting the ground, when I removed it works fine
    
    Answer:
    This is a classic ArduPilot SITL vs. MAVSDK conflict. You are absolutely correct to remove it.

    Here is exactly why await drone.action.hold() caused your drone to crash, and why simply removing it is the right fix.

    The Technical Reason: The "Phantom" Throttle
    Mode Switching: When you run drone.action.hold(), MAVSDK commands the drone to switch into LOITER mode.

    How LOITER Works: In ArduPilot, LOITER is a "Pilot Assisted" mode. It uses the GPS to hold position, BUT it looks at your Remote Controller (RC) Throttle stick to decide altitude.

    Stick Middle = Hover.

    Stick Down = Descend.

    The SITL Problem: Since you are running a script without a real joystick connected, the simulated RC Throttle channel defaults to 1000 pwm (Minimum/Bottom).

    The Moment you Switch: The drone enters LOITER, sees the virtual throttle is at 0%, and immediately obeys the "command" to descend rapidly. That is why you saw it "Hit ground at 2.4 m/s".
    '''
    await asyncio.sleep(5.0)

    #await drone.action.set_return_to_launch_altitude(20.0) # this action specific for PX-4, does'nt work with ardupilot
    await drone.param.set_param_int("RTL_ALT", 2000) # ArduPilot uses 'RTL_ALT' parameter in CENTIMETERS.

    print("-- Initiating RTL")
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