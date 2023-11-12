import random
import csv
def GetRandomSyn(file_name):
  random_line = GetRandomLine(file_name)
  random_line = random_line.upper() 
  lst_line = random_line.split(",")
  chosen = lst_line[0]
  lst_syns=[]
  for i in range(1,len(lst_line),2):
      s = [lst_line[i],int(lst_line[i+1])]
      lst_syns.append(s)
  return chosen,lst_syns  
  
def ReadCSV(filename):
    with open(filename, mode ='r')as file:
       csvFile = list(csv.reader(file))
    return csvFile 
           
def GetRandomLine(file_name):
    with open(file_name,"r") as f:
        L1=f.read().splitlines()
    print(len(L1))    
    return random.choice(L1)
def GetAllWords(file_name):
    with open(file_name,"r") as f:
        L1=f.read().splitlines()
    return L1  
def GetRandomColor():
  
  color = random.randrange(0, 2**24)
  hex_color = hex(color)
  std_color = "#" + hex_color[2:]
  return std_color
  