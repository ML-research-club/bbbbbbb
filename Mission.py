from __future__ import print_function
from builtins import range
import MalmoPython
import os
import sys
import time
import json
import uuid
import random

NUM_AGENTS = 2

#Set environmental variable for Schemas
os.environ['MALMO_XSD_PATH'] = "malmo/Schemas"

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

class Mission:
    def __init__(self, mission_xml, num_agents):
        self.mission = MalmoPython.MissionSpec(mission_xml, True)
        self.mission_record = MalmoPython.MissionRecordSpec()
        self.num_agents = num_agents
        self.experiment_ID = str(uuid.uuid4())
        self.client_pool = MalmoPython.ClientPool()
        for x in range(10000, 10000 + NUM_AGENTS + 1):
            self.client_pool.add( MalmoPython.ClientInfo('127.0.0.1', x) )

        # Create one agent host for parsing
        self.agent_hosts = [MalmoPython.AgentHost()]

        try:
            self.agent_hosts[0].parse( sys.argv )
        except RuntimeError as e:
            print('ERROR:',e)
            print(self.agent_hosts[0].getUsage())
            exit(1)
        if self.agent_hosts[0].receivedArgument("help"):
            print(self.agent_hosts[0].getUsage())
            exit(0)

        # Create the rest of the agent hosts.
        if self.num_agents > 1:
            self.agent_hosts += [MalmoPython.AgentHost() for x in range(NUM_AGENTS - 1) ]

    # Create default Malmo objects:
    def startMission(self):
        # Start the mission for every agent:
        for i in range(self.num_agents):
            used_attempts = 0
            max_attempts = 5
            print("Starting mission for role", i)
            while True:
                try:
                    # Attempt start:
                    self.agent_hosts[i].startMission(self.mission, self.client_pool, self.mission_record, i, self.experiment_ID)
                    break
                except MalmoPython.MissionException as e:
                    errorCode = e.details.errorCode
                    if errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_WARMING_UP:
                        print("Server not quite ready yet - waiting...")
                        time.sleep(2)
                    elif errorCode == MalmoPython.MissionErrorCode.MISSION_INSUFFICIENT_CLIENTS_AVAILABLE:
                        print("Not enough available Minecraft instances running.")
                        used_attempts += 1
                        if used_attempts < max_attempts:
                            print("Will wait in case they are starting up.", max_attempts - used_attempts, "attempts left.")
                            time.sleep(2)
                    elif errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_NOT_FOUND:
                        print("Server not found - has the mission with role 0 been started yet?")
                        used_attempts += 1
                        if used_attempts < max_attempts:
                            print("Will wait and retry.", max_attempts - used_attempts, "attempts left.")
                            time.sleep(2)
                    else:
                        print("Other error:", e.message)
                        print("Waiting will not help here - bailing immediately.")
                        exit(1)
                if used_attempts == max_attempts:
                    print("All chances used up - bailing now.")
                    exit(1)
            print("startMission called okay.")

        # Attempt to start the mission:
        print("Waiting for the mission to start", end=' ')
        start_flags = [False for a in self.agent_hosts]
        start_time = time.time()
        time_out = 10  # Allow a two minute timeout.
        while not all(start_flags) and time.time() - start_time < time_out:
            states = [a.peekWorldState() for a in self.agent_hosts]
            start_flags = [w.has_mission_begun for w in states]
            errors = [e for w in states for e in w.errors]
            if len(errors) > 0:
                print("Errors waiting for mission start:")
                for e in errors:
                    print(e.text)
                print("Bailing now.")
                exit(1)
            time.sleep(0.1)
            print(".", end=' ')
        if time.time() - start_time >= time_out:
            print("Timed out while waiting for mission to start - bailing.")
            exit(1)
        print()
        print("Mission has started.")

        print()
        print("Mission running")

        return self.agent_hosts

    def getYaw(self, agent):
        world_state = agent.getWorldState()
        # Wait until we are able to get a world state with new observations.
        while world_state.number_of_observations_since_last_state == 0:
            world_state = agent.getWorldState()
            time.sleep(0.1)
        observation = json.loads(world_state.observations[-1].text)
        return observation.get("Yaw")

    def rotate(self, agent, turnSpeed):
        agent.sendCommand("turn " + str(turnSpeed / 360))
        agent.getWorldState()

    def stopRotation(self, agent):
        agent.sendCommand("turn 0")
        agent.getWorldState()

    def newRotation(self, agent):
        turnSpeed = (random.random() * 360 - 180) / 360
        agent.sendCommand("turn " + str(turnSpeed))
        time.sleep(1)
        agent.sendCommand("turn 0")

    def getBlock(self, agent):
        world_state = agent.getWorldState()
        # Wait until we are able to get a world state with new observations.
        while world_state.number_of_observations_since_last_state == 0:
            world_state = agent.getWorldState()
            time.sleep(0.1)
        observation = world_state.observations[-1]
        return observation
