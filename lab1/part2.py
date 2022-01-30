import matplotlib.pyplot as plt
import queue
import random

# class for data packet
class Packet:
    def __init__(self, pid, sid, gtime=0.0):
        self.packetId = pid  # packet id
        self.sourceId = sid  # which source its from
        self.created = gtime  # which time it was generated
        self.qInTime = -1  # when it joined the queue
        self.qOutTime = -1  # when it left the queue
        self.sinkReachTime = -1  # when it finally reached sink

# class for data source
class Source:
    def __init__(self, sid, genrate, bandwidth) -> None:
        self.sourceId = sid  # source id
        self.generationRate = genrate  # generation rate of packets
        self.bandwidth = bandwidth  # bandwidth from source to switch

# class for data switch
class Switch:
    def __init__(self, bandwidth) -> None:
        self.bandwidth = bandwidth  # bandwidth from switch to sink
        self.queueSize = 0  # queue size at a particular instant

# there are 4 events in this simulation: packet generation (eid=0),
# joining into queue (1), leaving queue (2) and finally reaching sink (3)
class Event:
    def __init__(self, eid, pid, time) -> None:
        self.eventId = eid   # event id
        self.packetId = pid  # which packet it belongs to
        self.curTime = time  # event time

    # sort events based on current time in priority queue
    def __lt__(self, other):
        return self.curTime < other.curTime

# call function to simulate all events
def simulateNetwork(nSources, bSource, bSwitch, pGenRate, qSize, simTime):
    inRate = outRate = pLost = 0
    packets = []
    ptotal = 10
    switch = Switch(bSwitch)  # initialize switch
    # since transmission delay is inversely proportional to bandwidth
    transmissionDelay = 1/bSwitch
    # initialize priority queue for events (sorting based on time)
    pq = queue.PriorityQueue()
    time = 0.0

    # initial generation of 10 packets
    for i in range(ptotal):
        packets.append(Packet(i, random.randint(0, nSources-1), time))
        pq.put(Event(0, i, time))
        time += 0.0001

    lastLeft = -1  # time at which last packet left queue
    curtime = 0  # current time of event

    # while all packets do not reach sink and simulation time is not up
    while not pq.empty() and curtime < simTime:
        ev = pq.get()
        eid = ev.eventId
        pid = ev.packetId
        curtime = ev.curTime

        if eid == 0:
            # pid packet generated
            sid = packets[pid].sourceId

            # generate another packet from same source with generation rate = packet sending rate
            packets.append(Packet(ptotal, sid, curtime + 1/pGenRate))
            pq.put(Event(0, ptotal, curtime + 1/pGenRate))
            ptotal += 1  # increment total packets

            # generate event for expected arrival into queue by packet
            pq.put(Event(1, pid, curtime+(1/bSource)))
            packets[pid].qInTime = curtime+(1/bSource)
            #print("Packet {0} generated - {1}".format(pid, curtime))

        elif eid == 1:
            # packet entered queue (curtime = packets[pid].qInTime)
            inRate = (pid+1)/curtime  # arrival rate
            qCurSize = switch.queueSize

            # if queue is not filled send else discard it
            if(qCurSize < qSize):
                # if no other packet exists in queue, there is no delay
                if(qSize == 0):
                    packets[pid].qOutTime = curtime + transmissionDelay
                # otherwise it depends on the packet left before
                else:
                    packets[pid].qOutTime = lastLeft + transmissionDelay
                lastLeft = packets[pid].qOutTime
                # create event with expected queue leaving time
                pq.put(Event(2, pid, packets[pid].qOutTime))
                switch.queueSize += 1
            else:
                pLost += 1
            #print("Packet {0} entered queue - {1}".format(pid, curtime))

        elif eid == 2:
            # packet left queue (curtime = packets[pid].qOutTime)
            outRate = (pid+1-pLost)/curtime  # system transmission cap
            switch.queueSize -= 1
            packets[pid].sinkReachTime = packets[pid].qOutTime + (1/bSwitch)
            pq.put(Event(3, pid, packets[pid].sinkReachTime))
            #print("Packet {0} left queue -{1}".format(pid, curtime))
        else:
            # packet reached sink
            continue
            #print("Packet {0} reached sink - {1}".format(pid, curtime))

    pLossRate = pLost/ptotal  # packet loss rate = packets lost/ packets generated
    # utilization factor = arrival rate/ system transmission capacity
    utilFactor = inRate/bSwitch
    return (pLossRate, utilFactor)


def main():
    # hard coded values for network simulation
    NSOURCES = 4
    BSOURCE = 500  # packets/sec
    BSWITCH = 200  # packets/sec
    MINPGENRATE = 10  # packets/sec
    MAXPGENRATE = 400  # packets/sec
    QSIZE = 50  # packets
    SIMTIME = 10  # sec
    x = []
    y = []

    # vary packet sending rate to plot graph
    RATE = MINPGENRATE
    while RATE <= MAXPGENRATE:
        pLossRate, utilFactor = simulateNetwork(
            NSOURCES, BSOURCE, BSWITCH, RATE, QSIZE, SIMTIME)
        x.append(utilFactor)
        y.append(pLossRate)
        print(utilFactor, pLossRate)
        RATE += 10

    # plot graph
    plt.plot(x, y)
    plt.xlabel("Utilization Factor")
    plt.ylabel("Packet Loss Rate")
    plt.text(x[0], y[0], " #sources=4, bandwidth_ns=500packets/s,\n bandwidth_ss=200packets/s, simulation_time=10s\n queue_size=50packets, packet generation rate is varied")
    plt.title("Packet Loss Rate vs Utilization Factor")
    plt.show()


if __name__ == "__main__":
    main()
