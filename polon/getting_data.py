import csv

myFieldnames = ['patentID', 'date', 'region', 'title', 'type', 'authors', 'institut']
myFieldnames2 = list(myFieldnames)
myFieldnames2.append('publicists')

def createCsvWithoutEmptyCells(filename, fieldnames=myFieldnames):
    with open(filename, encoding='utf-8') as inp, open('clean'+filename, 'w', encoding='utf-8') as out:
        writer = csv.DictWriter(out, fieldnames=fieldnames, lineterminator='\n')
        lastIndex = fieldnames[len(fieldnames)-1]
        for row in csv.DictReader(inp, fieldnames=fieldnames):
            if row[lastIndex] != None:
                writer.writerow(row)

def createCsvWithPatentType(filename, type, fieldnames=myFieldnames):
    with open(filename, encoding='utf-8') as inp, open(type + '.csv', 'w', encoding='utf-8') as out:
        writer = csv.DictWriter(out, fieldnames=fieldnames, lineterminator='\n')
        for row in csv.DictReader(inp, fieldnames=fieldnames):
            if row['type'] == type:
                writer.writerow(row)

def createCsvByCopying(oldFilename, newFilename, fieldnames=myFieldnames):
    if(oldFilename == newFilename):
        return
    with open(oldFilename, encoding='utf-8') as inp, open(newFilename, 'w', encoding='utf-8') as out:
        writer = csv.DictWriter(out, fieldnames=fieldnames, lineterminator='\n')
        for row in csv.DictReader(inp, fieldnames=fieldnames):
            writer.writerow(row)

def getDistinctPatentTypes(filename, fieldnames=myFieldnames):
    types = []
    with open(filename, encoding='utf-8') as csvFile:
        reader = csv.DictReader(csvFile, fieldnames=fieldnames)
        for row in reader:
            if row['type'] not in types:
                types.append(row['type'])
        return types

def getPatentByID(filename, patentID, fieldnames=myFieldnames):
    with open(filename, encoding='utf-8') as csvFile:
        reader = csv.DictReader(csvFile, fieldnames=fieldnames)
        for row in reader:
            if row['patentID'] == patentID:
                return row

def getPatentByRow(filename, rowId, fieldnames=myFieldnames):
    if(rowId > getAllPatentsNumber(filename) or rowId < 0):
        rowId = 1
    with open(filename, encoding='utf-8') as csvFile:
        reader = csv.DictReader(csvFile, fieldnames=fieldnames)
        for row in reader:
            if reader.line_num == rowId:
                return row

def getPatentsList(filename, fieldnames=myFieldnames):
    patents = []
    with open(filename, encoding='utf-8') as csvFile:
        reader = csv.DictReader(csvFile, fieldnames=fieldnames)
        for row in reader:
            patents.append(row)
        return patents

def getAllPatentsNumber(filename):
    return sum(1 for row in open(filename, encoding='utf-8'))

def addRow(filename, patentRow):
    with open(filename, 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(patentRow)

#createCsvWithoutEmptyCells('patents.csv')
#print(getDistinctPatentTypes('cleanpatents.csv'))
#createCsvWithPatentType('cleanpatents.csv', 'Technologia')
#print(getPatentByID('Wynalazek.csv', '213836').get('title'))
# print(getPatentByRow('Technologia.csv', 1))
# print(getPatentByRow('Technologia.csv', 1).get('authors'))

#print((getPatentsList('Technologia.csv')[0]['patentID']))

#createCsvByCopying('Technologia.csv', 'test.csv')
#addRow('test.csv', myFieldnames2)
