# Helper Python File to convert the ledger format of an extracted Google Sheets CSV 
# to JSON files that can be used by D3.
# Cols: 
# 0:Empty 1:Payer 2:Amount 3:Payee 4:Shop 5:Uploader 6:Medium 7:Upload date 8:Notes 9-11:Trackers
import csv
import os
import json
import datetime

csvfile = open(os.getcwd()+'/assets/data/ledger.csv', 'r', newline='')
payers = {}
payees = {}
data = {
    "nodes":[],
    "links":[]
}
id = 0
for row in csvfile:
    row_arr = row.split(',')
    if row_arr[1] != 'Payer' : # Ignore the header row
        if row_arr[1] not in payers and row_arr[1] != '':
            payers[row_arr[1]] = id
            data['nodes'].append({"node":id,"name":row_arr[1]})
            id += 1
        if row_arr[3] not in payees and row_arr[3] != '':
            payees[row_arr[3]] = id
            data['nodes'].append({"node":id,"name":row_arr[3]})
            id += 1
        try:
            data['links'].append({"source": payers[row_arr[1]], "target": payees[row_arr[3]], "value": float(row_arr[2])})
        except Exception as E:
            pass

# with open(os.getcwd()+"/assets/data/sankey.json","w") as outfile:
#     outfile.write(json.dumps(data, indent=4))
#     print("Sankey JSON saved to disk")

del data
del payers
del payees

hermits = []
streamTotal = {}
videoTotal = {}
csvfile.seek(0)
for row in csvfile:
    row_arr = row.split(',')
    if row_arr[1] != 'Payer' and row_arr[1]!="": # Ignore the header row
        if row_arr[1] not in hermits and row_arr[3] != '':
            hermits.append(row_arr[1])
            streamTotal[row_arr[1]] = 0
            videoTotal[row_arr[1]] = 0
        if row_arr[3] not in hermits and row_arr[3] != '':
            hermits.append(row_arr[3])
            streamTotal[row_arr[3]] = 0
            videoTotal[row_arr[3]] = 0
        if row_arr[6] == "Stream":
            streamTotal[row_arr[1]] = float(row_arr[2])
        else:
            videoTotal[row_arr[1]] = float(row_arr[2])

data = []
i = 0
for hermit in hermits:
    i+=5
    data.append({"name":hermit,"medium":"stream", "amount":streamTotal[hermit], "index":i})
    data.append({"name":hermit,"medium":"video", "amount":videoTotal[hermit],"index":i})
# with open(os.getcwd()+"/assets/data/pyramid.json","w") as outfile:
#     outfile.write(json.dumps(data, indent=4))
#     print("Pyramid JSON saved to disk")

del data
del streamTotal
del videoTotal

data = {}
running_total = dict.fromkeys(hermits, 0)
csvfile.seek(0)

for row in csvfile:
    row_arr = row.split(',')
    if row_arr[1] != 'Payer' and row_arr[1]!="": # Ignore the header row
        date = datetime.datetime.strptime(row_arr[7], '%Y-%m-%d') 
        month_year_str = date.strftime('%B %Y')
        if month_year_str not in data:
            data[month_year_str] = []
            for hermit in hermits:
                data[month_year_str].append({"Hermit":hermit,"Total":running_total[hermit]})
        running_total[row_arr[3]] += float(row_arr[2])
        data[month_year_str][hermits.index(row_arr[3])]["Total"] += float(row_arr[2])

# with open(os.getcwd()+"/assets/data/racing_bars.json","w") as outfile:
#     outfile.write(json.dumps(data, indent=4))
#     print("Transactions JSON saved to disk")
csvfile.seek(0)
data = {}
for row in csvfile:
    row_arr = row.split(',')
    if row_arr[1] != 'Payer' and row_arr[1]!="":
        shop = row_arr[4]
        if (shop == "Octagon" and "log" in row_arr[8].lower()):
            shop = "Logz"
        if (shop == "Horse Head Farms" and "iou" in row_arr[8].lower()):
            shop = "IOU"
        if shop not in data:
            data[shop] = float(row_arr[2])
        else:
            data[shop] += float(row_arr[2])


masterData = {
    "children":[
        {"name":"Boatem",
            "children":[
                {"name":"G-Train","value":round(data["G-Train"])},
                {"name":"Potato vending Machine","value":round(data["Potato Vending Machine"])},
                {"name":"iSoar","value":round(data["iSoar"])},
                {"name":"Padllama Co.","value":round(data["Padllama Co."])},
                {"name":"Harmless Harvests","value":round(data["Harmless Harvests"])},
                {"name":"Bee Shop","value":round(data["Bee Shop"])},
                {"name":"iFloatem","value":round(data["iFloatem"])},
                {"name":"Swaggon","value":round(data["Swaggon"])},
                {"name":"Lichen Subscribe","value":round(data["Lichen Subscribe"])},
                {"name":"Nether Wood iEver","value":round(data["Impulse's Nether Wood iEver"])},
                {"name":"Cheapslate","value":round(data["Cheapslate"])},
                {"name":"iCandy","value":round(data["iCandy"])},
                {"name":"Vol-Carb-o","value":round(data["Vol-Carb-o"])},
                {"name":"Shopwreck","value":round(data["Shopwreck"])},

            ]
        },
        {
            "name":"Octagon",
            "children":[
                {"name":"Shulker Walker","value":round(data["Shulker Walker"])},
                {"name":"Octagon","value":round(data["Octagon"])},
                {"name":"Derpcoin ATM","value":round(data["Octagon Derpcoin ATM"])/2},
                {"name":"Logz","value":round(data["Logz"])},
            ]
        },
        {
            "name":"Big Eyes",
            "children":[
                {"name":"Big Eyes Pass N Gas","value":round(data["Big Eyes Pass N Gas"])},
                {"name":"Basalt","value":round(data["Big Eyes Basalt"])},
                {"name":"Copper n Candles","value":round(data["Copper n Candles"])},
            ]
        },
        {
            "name":"Evil Emporium",
            "children":[
                {"name":"Evil Emporium","value":round(data["Evil Emporium"])},
                {"name":"Derpcoin Spinner ","value":round(data["Evil Gambling"])},
                {"name":"Derpcoin ATM","value":round(data["Octagon Derpcoin ATM"])/2},
            ]
        },
        {
            "name":"Horse Head Farms",
            "children":[
                {"name":"Horse Head Farms","value":round(data["Horse Head Farms"])},
                {"name":"IOU Auction","value":round(data["IOU"])},
            ]
        },
    ]
}
with open(os.getcwd()+"/assets/data/treemapN.json","w") as outfile:
    for districts in masterData["children"]:
        districtSum = 0
        print(districts)
        for hermit in districts["children"]:
            print(hermit)
            districtSum += hermit["value"]
        districts["value"]=districtSum
    outfile.write(json.dumps(masterData, indent=4))