from Mission import Mission
import time
import NEAT

# Set the number of agents that will be used.
NUM_AGENTS = 1

# Build the XML for the diamondPillar mission.
missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
              <About>
                <Summary>Hello world!</Summary>
              </About>
              <ModSettings>
                <MsPerTick>50</MsPerTick>
              </ModSettings>
              <ServerSection>
                <ServerInitialConditions>
                    <Time>
                        <StartTime>12000</StartTime>
                        <AllowPassageOfTime>false</AllowPassageOfTime>
                    </Time>
                </ServerInitialConditions>
                <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,54*3,2;1;"/>
                  <DrawingDecorator>
                    <DrawLine x1="0" y1="56" z1="0" x2="0" y2="60" z2="0" type="diamond_block"/>
                  </DrawingDecorator>
                  <ServerQuitFromTimeUp description="" timeLimitMs="50000"/>
                </ServerHandlers>
              </ServerSection>'''

for n in range(NUM_AGENTS):
    missionXML +='''<AgentSection mode="Survival">
                        <Name>''' + str(n) + '''</Name>
                        <AgentStart>
                            <Placement x="5.5" y="56" z = "0.5" yaw="0"/>
                        </AgentStart>
                        <AgentHandlers>
                            <ObservationFromFullStats/>
                            <ObservationFromMultiRay/>
                            <MissionQuitCommands/>
                            <ContinuousMovementCommands turnSpeedDegs="360"/>
                        </AgentHandlers>
                    </AgentSection>'''

missionXML += '''</Mission>'''

mission = Mission(missionXML, NUM_AGENTS)

# agent: Agent
agents = mission.startMission()
print(agents)
agent = agents[0]

# Yaw is left and right
# getYaw takes an agent and returns that agent's yaw. Yaws between 86 and 94 will be looking at the diamond pillar.
print(mission.getYaw(agent))


# rotate takes an agent and a number d, and rotates the agent d degrees on yaw axis. -360 <= d <= 360
# rotate will pause your program for the 1 second it takes to process. This is because idk how to multithread stuff.
mission.rotate(agent, 5)
print(mission.getYaw(agent))


# newRotation takes an agent and rotates it so it will be facing a random direction.
mission.newRotation(agent)
print(mission.getYaw(agent))


def fitness(nn):
	global agent
	global mission
	totalTries = 25
	tickNumber = 0
	print("Randomizing")
	mission.newRotation(agent)
	print("Done randomizing")
	while tickNumber < totalTries:
		mission.rotate(agent, nn.computeOutput([mission.getYaw(agent), 90])[0])
		tickNumber += 1
	mission.stopRotation(agent)
	fit = mission.getYaw(agent) - 90
	print("fitness is: {}.".format(mission.getYaw(agent) - 90))
	print(mission.getBlock(agent))
	return mission.getYaw(agent) - 90

class Generation:
	#constructor(prev: Generation, genSize: integer, numInputs: integer, numOutputs: integer): Generation
	def __init__(self, prev=None, genSize=None, numInputs=2, numOutputs=1):
		if prev == None:
			self.nns = []
			for i in range(genSize):
				self.nns.append(NEAT.NeuralNetwork(numInputs, numOutputs))
			self.size = genSize
		else:
			self.size = prev.size
			self.nns = []
			prev.nns.sort(key=lambda x: -1 * fitness(x))
			for i in prev.nns[:int(len(prev.nns) // 4)]:
				copy = i.copy()
				copy.mutate()
				self.nns.append(copy)
				copy = i.copy()
				copy.mutate()
				self.nns.append(copy)
				copy = i.copy()
				copy.mutate()
				self.nns.append(copy)
				copy = i.copy()
				copy.mutate()
				self.nns.append(copy)

gen = Generation(genSize=20)
gen = Generation(prev=gen)
gen = Generation(prev=gen)
gen = Generation(prev=gen)
