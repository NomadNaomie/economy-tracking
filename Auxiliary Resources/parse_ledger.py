# Helper Python File to convert the ledger format of an extracted Google Sheets CSV 
# to JSON files that can be used by D3.
# Cols: 
# 0:Empty 1:Payer 2:Amount 3:Payee 4:Shop 5:Uploader 6:Medium 7:Upload date 8:Notes 9-11:Trackers
import csv
import os
import json

csvfile = open('../assets/data/ledger.csv', 'r', newline='')
payers = {}
payees = {}
data = {
    "nodes":[],
    "links":[]
}
id = 0
for row in csvfile:
    row_arr = row.split(',')
    if row_arr[1] != 'Payer': # Ignore the header row
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

with open("../assets/data/sankey.json","w") as outfile:
    outfile.write(json.dumps(data, indent=4))
    print("Sankey JSON saved to disk")

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
with open("../assets/data/pyramid.json","w") as outfile:
    outfile.write(json.dumps(data, indent=4))
    print("Pyramid JSON saved to disk")