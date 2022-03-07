import numpy as np


G = [(2,2),(4,0),(0,4),(1,1)]
P = []
BargainingSteps = 500

R = [r for r,c in G]
C = [c for r,c in G]

print("Game: " + str(G))
print("Utilities, R: " + str(R))
print("Utilities, C: " + str(C))


def InitialProbs(P,R):
    l1 = len(P)
    if l1 == 0:
        for i in range(len(R)):
            a = 1/len(R)
            P.append(a)
        else:
            return P
    return P

P = InitialProbs(P,G)
print("Initial probs: " + str(P))

def updateP(probs,utils):

    def equalizer(list):
        elementnum = 0
        negatives = []
        positives = []
        for element in list:
            if element < 0:
                negatives.append(element)
                elementnum = elementnum + 1
            else:
                positives.append(element)
                elementnum = elementnum + 1

        allN = (np.sum(negatives)) * -1
        allP = np.sum(positives)

        equalizedList = []
        elementnum = 0
        #print(list)
        for element in list:
            if element < 0:
                equalizedList.append(element)
                elementnum = elementnum + 1
            else:
                num = (allN / allP) * element
                equalizedList.append(num)
                elementnum = elementnum + 1
        squashRatio = 0.1 / (allP + allN)

        #print(equalizedList)
        squashedlist = []
        for element in equalizedList:
            element = element * squashRatio
            squashedlist.append(element)

        return squashedlist

    def SignsMaker(list):
        elementnum = 0
        listSigns = []
        for element in list:
            if element < 0:
                sign = -1
                listSigns.append(sign)
                elementnum = elementnum + 1
            else:
                sign = 1
                listSigns.append(sign)
                elementnum = elementnum + 1

        # print("listSigns:" + str(listSigns))
        return listSigns


    def AbsoluteList(list):
        elementnum = 0
        absoluteList = []
        for element in list:
            if element < 0:
                a = list[elementnum]*(-1)
                #print(a)
                absoluteList.append(a)
                elementnum = elementnum + 1
            else:
                absoluteList.append(element)
                elementnum = elementnum + 1
        #print("absolutelist:" + str(absoluteList))
        return absoluteList

    exU = np.multiply(utils, probs)
    averageexU = np.sum(exU) / len(exU)

    deviation = exU - averageexU

    # This is to avoid negative probs, it makes the prob tweaks super small when they approach zero,
    # But I think it also creates an imbalance, where the agent who goes first gets more power,
    # as they will have a higher multiplier for the probs they prefer
    deviation = deviation * probs


    absoluteDeviation = AbsoluteList(deviation)

    proportionsAbsoluteList = absoluteDeviation/(np.sum(absoluteDeviation))

    #This is to remember the direction probs should be tweaked, as this information is lost during absolution
    deviationSigns = SignsMaker(deviation)

    proportionsAbsoluteList = np.multiply(proportionsAbsoluteList,deviationSigns)

    #print("oldprobs:" + str(probs))

    probChanges = equalizer(proportionsAbsoluteList)

    sumprobchanges = np.sum(probChanges)

    probChanges = np.array(probChanges)
    probs = probs + probChanges

    #print("Prob changes:" + str(probChanges))
    #print("Sum prob changes:" + str(sumprobchanges))
    #print("new probs: " + str(probs))

    return probs

for i in range(BargainingSteps):
    P = updateP(P,R)
    P = updateP(P,C)

P1 = P
P = InitialProbs(P,R)
for i in range(BargainingSteps):
     P = updateP(P,C)
     P = updateP(P,R)

print("Bargaining completed after " + str(BargainingSteps) + " steps.")
print("Final Probabilities, R starts:" + str(P1))
print("Final Probabilities, C starts:" + str(P))

GelementOutput = int(np.random.choice([0,1,2,3], 1, p=P))
result = G[GelementOutput]

print("Cell " + str(GelementOutput) + " of game " + str(G) + " has been selected.")
print("Final outcome of event (R,C): " + str(result))
