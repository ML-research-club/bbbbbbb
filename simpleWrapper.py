import diamondPillar
import time
import NEAT

# agent: Agent
agent = diamondPillar.startMission()

# Yaw is left and right
# getYaw takes an agent and returns that agent's yaw. Yaws between 86 and 94 will be looking at the diamond pillar.
print(diamondPillar.getYaw(agent))


# rotate takes an agent and a number d, and rotates the agent d degrees on yaw axis. -360 <= d <= 360
# rotate will pause your program for the 1 second it takes to process. This is because idk how to multithread stuff.
diamondPillar.rotate(agent, 5)
print(diamondPillar.getYaw(agent))


# newRotation takes an agent and rotates it so it will be facing a random direction.
diamondPillar.newRotation(agent)
print(diamondPillar.getYaw(agent))


def fitness(nn):
	global agent
	global diamondPillar
	totalTries = 25
	tickNumber = 0
	print("Randomizing")
	diamondPillar.newRotation(agent)
	print("Done randomizing")
	while tickNumber < totalTries:
		diamondPillar.rotate(agent, nn.computeOutput([diamondPillar.getYaw(agent), 90])[0])
		tickNumber += 1
	diamondPillar.stopRotation(agent)
	fit = diamondPillar.getYaw(agent) - 90
	print("fitness is: {}.".format(diamondPillar.getYaw(agent) - 90))
	print(diamondPillar.getBlock(agent))
	return diamondPillar.getYaw(agent) - 90

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
