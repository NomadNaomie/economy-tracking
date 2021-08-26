# Helper Python File to convert the ledger format of an extracted Google Sheets CSV 
# to a JSON file that can be used by D3.
# For use with Sankey.js  
#
import csv
import os
csvfile = open('ledger.csv', 'r', newline='')
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
            print("{0} at row {1}".format(  E, row_arr[0]))

with open("sankey.json","w") as outfile:
    outfile.write(str(data))
