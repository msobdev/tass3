import csv

rownum = 0
with open('patentall.csv', newline='', encoding='utf-8') as myFile:
    reader = csv.reader(myFile)
    for row in reader:
        print(row)
        rownum+=1
        if(rownum >= 10):
            break