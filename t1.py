import os
import pandas as pd
from decimal import Decimal
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
matplotlib.use('TkAgg')

# Use structures to store each transaction
class NodeLyt(object):
    def __init__(self, timestamp, price, loyaltynum):
        self.timestamp = timestamp
        self.price = price
        self.loyaltynum = loyaltynum

class NodeCC(object):
    def __init__(self, timestamp, price, last4ccnum):
        self.timestamp = timestamp
        self.price = price
        self.loyaltynum = last4ccnum

# calculate the sum of price in two documents
def calSumCsp(fileLyt,fileCC):
    sumPriceLyt = Decimal(0.0)
    sumPriceCC  = Decimal(0.0)

    # read two files
    for i in range(len(dfLyt)):
        document = dfLyt[i:i + 1]
        PriceLyt = str(document['price'][i])
        sumPriceLyt += Decimal(PriceLyt)

    for i in range(len(dfCC)):
        document = dfCC[i:i + 1]
        PriceCC = str(document['price'][i])
        sumPriceCC += Decimal(PriceCC)

    print(sumPriceLyt)
    print(sumPriceCC)

# read csv to dict
def readLyt(dfLyt):
    placeListLyt = {}
    for i in range(len(dfLyt)):
        document = dfLyt[i:i + 1]
        # node
        place = str(document['location'][i])
        node = NodeLyt(document['timestamp'][i], document['price'][i], document['loyaltynum'][i])

        # place in Dict placeList? add node into the list
        if placeListLyt.get(place, None) != None:
            placeListLyt[place].append(node)
        else:
            placeListLyt[place] = []
            placeListLyt[place].append(node)
    return placeListLyt

def readCC(dfCC):
    placeListCC = {}
    # 从文件中读取信息放入placeListCC
    for i in range(len(dfCC)):
        document = dfCC[i:i + 1]
        # node
        place = str(document['location'][i])
        node = NodeCC(document['timestamp'][i], document['price'][i], document['last4ccnum'][i])

        # place in Dict placeList? add node into the list
        if placeListCC.get(place, None) != None:
            placeListCC[place].append(node)
        else:
            placeListCC[place] = []
            placeListCC[place].append(node)
    return placeListCC

# calculate total consumption and the distribution
def static(placeCat, cspCntSum, cspCostSum, cspCnt, cspCost, placeList):
    j = 0
    # for each place
    for key in placeCat:
        # initialize, use Decimal to calculate the amount
        cspCnt.append([0]*24)
        cspCost.append([Decimal(0)]*24)
        cspCntSum.append(0)
        cspCostSum.append(Decimal(0))
        # read the list, put into cspCntSum, cspCostSum, cspCnt, cspCost
        for i in range(len(placeList[placeCat[key]])):
            timestamp = placeList[placeCat[key]][i].timestamp
            price = str(placeList[placeCat[key]][i].price)
            tmp = timestamp.split(" ")
            # date = tmp[0]
            time = tmp[1]
            timeA = int(int(time.split(":")[0]) )
            cspCnt[j][timeA]  += 1
            cspCost[j][timeA] += Decimal(price)
            cspCntSum[j]  += 1
            cspCostSum[j] += Decimal(price)
        j += 1

    for i in range(len(cspCostSum)):
        cspCostSum[i] = float(cspCostSum[i])
    for i in range(len(cspCost)):
        for j in range(len(cspCost[i])):
            cspCost[i][j] = float(cspCost[i][j])

    return cspCntSum, cspCostSum, cspCnt, cspCost

# only calculate total consumption
def staticSum(placeCat, cspCntSum, cspCostSum, placeList):
    j = 0
    # for each place
    for key in placeCat:
        # initialize, use Decimal to calculate the amount
        cspCntSum.append(0)
        cspCostSum.append(Decimal(0))
        if placeList.get(placeCat[key]) == None:
            print(placeCat[key]+"in cc not in lyt")
            continue
        # read the list to learn the details and put them into cspCntSum, cspCostSum
        for i in range(len(placeList[placeCat[key]])):
            price = str(placeList[placeCat[key]][i].price)
            cspCntSum[j]  += 1
            cspCostSum[j] += Decimal(price)
        j += 1

    for i in range(len(cspCostSum)):
        cspCostSum[i] = float(cspCostSum[i])

    return cspCntSum, cspCostSum




if __name__ == '__main__':

    # read files
    fileLyt = pd.read_csv("../loyalty_data.csv",encoding='cp1252')
    fileCC  = pd.read_csv("../cc_data.csv",encoding='cp1252')
    dfLyt   = pd.DataFrame(fileLyt)
    dfCC    = pd.DataFrame(fileCC)

    # Are the two files same?
    calSumCsp(fileLyt,fileCC)


    # put the data into placeList
    # key--location, value--list of nodes, node(timestamp, price, peopleID)
    placeListLyt = readLyt(dfLyt)
    placeListCC  = readCC(dfCC)


    # categorize the place
    placeCat = {
 'Cafe BBS': "Brew've Been Served",
 'Cafe CS' : "Coffee Shack",
 'Cafe BTDT' : "Bean There Done That",
 'Cafe CC': "Coffee Cameleon",
 'Cafe JMB': "Jack's Magical Beans",
 'Cafe KC': "Katerina’s Café",
 'Cafe BA': "Brewed Awakenings",
 'Cafe HG': "Hallowed Grounds",
 'Food GG' : "Guy's Gyros",
 'Food OE': "Ouzeri Elian",
 'Food KK' : "Kalami Kafenion",
 'Relax DGC': "Desafio Golf Course",
 'Relax AFC': "Albert's Fine Clothing",
 'Relax SD': "Shoppers' Delight",
 'Relax AM': "Ahaggo Museum",
 'Relax G': "Gelatogalore",
 'Daily KM': "Kronos Mart",
 'Daily FF': "Frank's Fuel",
 'Daily AS': "Abila Scrapyard",
 'Daily GG': "General Grocer",
 'Daily KPI': "Kronos Pipe and Irrigation",
 'Daily DD': "Daily Dealz",
 'Daily UP': "U-Pump",
 'Travel CH': "Chostus Hotel",
 'Travel AA': "Abila Airport",
 'Company FAM': "Frydos Autosupply n' More",
 'Company MIS': "Maximum Iron and Steel",
 'Company SSF': "Stewart and Sons Fabrication",
 'Company CC': "Carlyle Chemical Inc.",
 'Company NR': "Nationwide Refinery",
 'Company OOS': "Octavio's Office Supplies",
 'Company RS': "Roberts and Sons",
 'Company H': "Hippokampos",
 'Company AZ': "Abila Zacharo"
}
    # arrange places in categories
    keyList = []
    for key in placeCat:
        keyList.append(key)
    print(keyList)

    # Store: location-cnt-time in cspCnt，location-amount-time in cspCost heatmap --- to find when popular
    cspCntCC  = []
    cspCostCC = []

    # Store: location-cnt in sum to cspCntSum，location-amount in sum to cspCostSum --- to find which is popular
    cspCntSumCC   = []
    cspCostSumCC  = []
    cspCntSumLyt  = []
    cspCostSumLyt = []


    # read dict to learn the details of consumption
    cspCntSumCC, cspCostSumCC, cspCntCC, cspCostCC = static(placeCat, cspCntSumCC, cspCostSumCC, cspCntCC, cspCostCC, placeListCC)

    cspCntSumLyt, cspCostSumLyt = staticSum(placeCat, cspCntSumLyt, cspCostSumLyt, placeListLyt)

    '''
    print("cc")
    print(cspCntSumCC)
    print(cspCostSumCC)
    print("lyt")
    print(cspCntSumLyt)
    print(cspCostSumLyt)
cc
[156, 8, 47, 38, 37, 212, 30, 92, 158, 87, 64, 8, 25, 20, 6, 64, 10, 2, 4, 10, 6, 1, 2, 9, 25, 47, 6, 18, 19, 24, 4, 8, 171, 72]
[3124.04, 123.64, 1077.89, 675.49, 800.67, 7286.37, 648.88, 1848.28, 5346.25, 3203.73, 2236.19, 1293.5, 5518.78, 3499.12, 464.32, 2329.67, 1863.98, 118.0, 9482.09, 1896.32, 13658.52, 2.01, 114.76, 1646.52, 68153.46, 17294.71, 16208.04, 40712.47, 43767.65, 43498.18, 466.97, 1572.18, 6675.9, 2859.25]
lyt
[140, 9, 45, 37, 35, 195, 29, 80, 146, 84, 66, 8, 25, 18, 6, 60, 8, 2, 4, 12, 6, 1, 8, 26, 42, 6, 17, 19, 23, 3, 6, 155, 71, 0]
[1519.56, 101.81, 541.63, 416.23, 425.02, 5405.31, 313.09, 961.66, 3808.07, 2451.08, 1871.91, 1233.5, 5438.78, 3052.47, 444.32, 1568.48, 1487.87, 118.0, 9482.09, 2077.08, 13618.52, 59.51, 1389.11, 69204.8, 6442.76, 16208.04, 38821.54, 43172.77, 44790.8, 335.24, 1169.04, 4533.18, 1969.54, 0.0]

'''

    # calculate total consumptions
    plt.barh(keyList, cspCntSumCC, color ='salmon')
    plt.title('Total consumption times')
    plt.xlabel('Times')
    plt.ylabel('Places')
    ax = plt.gca()
    ax.invert_yaxis()
    plt.show()

    plt.barh(keyList, cspCostSumCC, color ='#8CD17D')
    plt.xlabel('Amount')
    plt.ylabel('Places')
    ax = plt.gca()
    ax.invert_yaxis()
    plt.title('Total consumption amount')
    plt.show()

    # compare using CC and Lyt
    x = np.arange(34)
    width = 0.3
    plt.barh(x - width / 2, cspCntSumCC, height=width, color="salmon", label='CC')
    plt.barh(x + width / 2, cspCntSumLyt, height=width, color="burlywood", label='Lyt')
    ax = plt.gca()
    ax.invert_yaxis()
    plt.title('Total consumption times - using CC or Lyt')
    plt.yticks(x, labels=keyList)
    plt.legend()
    plt.show()


    # heatmap times
    sns.heatmap(cspCntCC, cmap='Reds', yticklabels=keyList, linewidths=.5)
    plt.title('Time distribution of consumption times')
    plt.xlabel('Time (o\' clock)')
    plt.ylabel('Places')
    plt.show()

    sns.heatmap(cspCostCC, cmap='Greens', yticklabels=keyList, linewidths=.5)
    plt.title('Time distribution of consumption amount')
    plt.xlabel('Time (o\' clock)')
    plt.ylabel('Places')
    plt.show()



