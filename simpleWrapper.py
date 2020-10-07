import diamondPillar
import time

agent = diamondPillar.startMission()
# getYaw takes an agent and returns that agent's yaw. Yaws between 86 and 94 will be looking at the diamond pillar.
print(diamondPillar.getYaw(agent))
# rotate takes an agent and a number d, and rotates the agent d degrees. -360 <= d <= 360
# rotate will pause your program for the 1 second it takes to process. This is because idk how to multithread stuff.
diamondPillar.rotate(agent, 5)
print(diamondPillar.getYaw(agent))
# newRotation takes an agent and rotates it so it will be facing a random direction.
diamondPillar.newRotation(agent)
print(diamondPillar.getYaw(agent))
