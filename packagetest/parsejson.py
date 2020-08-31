import json
import re
if __name__ == "__main__":
    f = open('./formrecog/test.json')   
    
    data = json.load(f)
    f = open('./formrecog/test.json',)   
    data = json.load(f)
    address = data['analyzeResult']['documentResults'][0]['fields']['Address']['valueString']
    ifsCode = re.split('IFS Code:', address)[1]
    date = data['analyzeResult']['documentResults'][0]['fields']['Date']['valueString']
    payee = data['analyzeResult']['documentResults'][0]['fields']['Payee']['valueString']
    amountWords = data['analyzeResult']['documentResults'][0]['fields']['AmountWords']['valueString']
    amountNumbers = data['analyzeResult']['documentResults'][0]['fields']['AmountNumbers']['valueString']
    micr = data['analyzeResult']['documentResults'][0]['fields']['Micr']['valueString']
    print("Address {} \n Date {} \n Payee {} \n Amount in Words {} \n Amount in Numbers {} \n IFS Code {} \n MICR {}".format(address, date, payee, amountWords, amountNumbers, ifsCode,micr))
    f.close()
