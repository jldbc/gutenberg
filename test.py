import sys
import fileinput


def something():
    maxValue = -10
    minValue = 100
    with open("hi.txt", "r") as f:
        for line in f:
            line = line.rstrip('\n')
            if (line.split(',')[2] > maxValue):
                maxValue = line.split(',')[2]
            temp = float(line.split(',')[2])
            if (temp < minValue):
                minValue = temp
        subtractValue = float(maxValue) - float(minValue)

    for line in fileinput.input('hi.txt', inplace=True):
        line = line.rstrip('\n')
        temp = float(line.split(',')[2])
        temp = (temp - minValue) / subtractValue
        newline = line.split(',')[0] + ',' + line.split(',')[1] + ',' + str(temp) + '\n' 
        line=line.replace(line, newline)
        print line.replace('line', 'newline'),

         
something()
