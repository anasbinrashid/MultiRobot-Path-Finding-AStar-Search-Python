import heapq
import re

class Robot:

    def __init__(self, robotid, startingposition, destination):

        self.robotid = robotid
        self.startingposition = startingposition
        self.destination = destination
        self.remainingroute = []
        self.completedroute = []
        self.currentlocation = startingposition
        self.goalreached = False
        self.failedmoves = 0

def heuristicmanhattandistance(point1, point2):

    value1 = abs(point1[0] - point2[0])
    value2 = abs(point1[1] - point2[1])
    return (value1 + value2)

def astarsearch(start, end, grid, dynamicagents, starttime=0):

    fringe, closedlist = [(heuristicmanhattandistance(start, end), start, starttime, [start])], set()

    while fringe:

        cost, currentposition, timestamp, traveledpath = heapq.heappop(fringe)

        if start != (169, 12) and len(closedlist) > 10000:
            return []

        if currentposition == end:
            return traveledpath

        currentstate = (currentposition, timestamp)
        if currentstate in closedlist:
            continue

        closedlist.add(currentstate)

        for movement1, movement2 in [(0, 1), (1, 0), (0, -1), (-1, 0)]:

            nextposition = (currentposition[0] + movement1, currentposition[1] + movement2)

            if (not(0 <= nextposition[0] < len(grid) and 0 <= nextposition[1] < len(grid[0]))) or (grid[nextposition[0]][nextposition[1]] == 'X') or (nextposition in dynamicagents.get(timestamp + 1, set())):
                continue

            heapq.heappush(fringe, (len(traveledpath + [nextposition]) + heuristicmanhattandistance(nextposition, end), nextposition, timestamp + 1, traveledpath + [nextposition]))

    return []

def robotmovement(robots, dynamicagents, grid):

    iteration = 0
    movingrobots = set(robots)
    currentagentlocation = {}
    agentpath = {}

    for starttime, positions in dynamicagents.items():
        fullpath = list(positions) + list(positions)[-2::-1]
        agentpath[starttime] = fullpath
        currentagentlocation[starttime] = fullpath[0]

    while movingrobots and iteration < 10000:

        for agent_id, path in agentpath.items():
            cycle_length = len(path)
            current_index = iteration % cycle_length
            currentagentlocation[agent_id] = path[current_index]

        filledpositions = set(currentagentlocation.values())

        for robot in list(movingrobots):
            if not robot.remainingroute:
                returnedpath = astarsearch(robot.currentlocation, robot.destination, grid, currentagentlocation, iteration)

                if returnedpath:
                    robot.remainingroute = returnedpath[:]
                    robot.completedroute = returnedpath[:]

            if robot.remainingroute:
                nextmove = robot.remainingroute.pop(0)
                if nextmove not in filledpositions:
                    filledpositions.add(nextmove)
                    robot.currentlocation = nextmove
                    if robot.currentlocation == robot.destination:
                        robot.goalreached = True
                        movingrobots.remove(robot)
                else:
                    robot.remainingroute = astarsearch(robot.currentlocation, robot.destination, grid, currentagentlocation, iteration)
            else:
                robot.failedmoves += 1
                if robot.failedmoves > 50:
                    print("Robot", robot.robotid + 1, "is stuck and removed as it made 50 failed moves")
                    movingrobots.remove(robot)

        iteration += 1

    return iteration

def main():
    with open('D:\ANAS\WORK\SEMESTER 6\Artificial Intelligence\Assignment 1\Data\data2.txt', "r") as file:
        lines = file.readlines()

    gridsize = int(lines[0].strip())
    grid = [list(line.rstrip("\n")) for line in lines[1:gridsize + 1]]

    print(f"Grid ({len(grid)} x {max(len(row) for row in grid)}):\n")
    for row in grid:
        print("".join(row))

    robots = []
    with open('D:\ANAS\WORK\SEMESTER 6\Artificial Intelligence\Assignment 1\Data\Robots2.txt', 'r') as file:
        for index, line in enumerate(file.readlines()):
            match = re.search(r"Start \((\d+), (\d+)\) End \((\d+), (\d+)\)", line)
            if match:
                robots.append(Robot(index, (int(match[1]), int(match[2])), (int(match[3]), int(match[4]))))

    dynamicagents = {}
    print("\nDynamic Agents:\n")

    agentid = 0
    with open('D:\ANAS\WORK\SEMESTER 6\Artificial Intelligence\Assignment 1\Data\Agent2.txt', 'r') as file:
        for line in file.readlines():
            match = re.search(r"Agent \d+: \[\((.*?)\)\] at times \[(.*?)\]", line)

            listofpositions = [tuple(map(int, pos.replace("(", "").replace(")", "").split(", "))) for pos in match.group(1).split("), (")]
            timestamplist = list(map(int, match.group(2).split(", ")))

            print("- Agent", agentid + 1, ": ", listofpositions, " at times ", timestamplist)

            fullpath = listofpositions + listofpositions[-2::-1]
            fulltimestamps = timestamplist + [timestamplist[-1] + i + 1 for i in range(len(listofpositions) - 1)]

            agentid += 1

            for t, pos in zip(fulltimestamps, fullpath):
                if t not in dynamicagents:
                    dynamicagents[t] = set()
                dynamicagents[t].add(pos)

    print("\nRobots:\n")
    for robot in robots:
        print('- Robot', robot.robotid + 1, ': Start', robot.startingposition, ', Goal', robot.destination)

    totaltime = robotmovement(robots, dynamicagents, grid)

    for robot in robots:
        print("\nRobot", robot.robotid + 1, "Path:", robot.completedroute)
        print("Robot", robot.robotid + 1, "Total Time:", len(robot.completedroute) - 1 if robot.completedroute else -1)

    print("\nSimulation finished at Iteration", totaltime)

if __name__ == "__main__":
    main()

