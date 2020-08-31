########### Python Form Recognizer Async Analyze #############
import json
import time
import getopt
import sys
import os
import re
from requests import get, post
from datetime import date


def validation(ifsCode, dateVal, payee, amountWords, amountNumbers, micr):
    inValidStr = 'Invalid'
    validStr = 'Valid'
    validation = {}
    #Strip any spaces
    
    ifsCode = ifsCode.replace(' ', '')
    if len(ifsCode) == 11:
        branchCode, branchNumber = ifsCode.split("0", 1)
        validation['ifsCode'] = validStr
    else:
        validation['ifsCode'] = inValidStr


    dateVal = dateVal.replace(' ', '')
    if len(dateVal) == 8:
        day, month, year = int(dateVal[:2]), int(dateVal[2:4]), int(dateVal[4:])
        today = date.today()
        cheqDate = date(year, month, day)
        diff = abs(cheqDate - today).days
        validation['dateVal'] = inValidStr if diff > 90 else validStr 
    else:
        validation['dateVal'] = inValidStr

    payeeCheck = payee.replace(' ', '').isalpha()
    validation['payee'] = validStr if payeeCheck else inValidStr

    amountWordsCheck = amountWords.replace(' ','').isalpha()
    validation['amountWords'] = validStr if amountWordsCheck else inValidStr

    amountNumbersCheck = amountNumbers.replace(' ', '').replace(',', '').replace('/','').replace('-','').isnumeric()
    validation['amountNumbers'] = validStr if amountNumbersCheck else inValidStr

    micrCheck = micr.replace(' ', '').isnumeric()
    validation['micr'] = validStr if micrCheck else inValidStr
    return validation




def entrymain(argumentsList):
    input_file, output_file, file_type = getArguments(argumentsList)
    okthisisthedict = runAnalysis(input_file, output_file, file_type)
    
    return okthisisthedict

def runAnalysis(input_file, output_file, file_type):

    # Endpoint URL
    endpoint = r"https://checkocr.cognitiveservices.azure.com/"
    # Subscription Key
    apim_key = "58a57325dccf4adeb7e7f76ded98ffb3"
    # Model ID
    # model_id = "adc7d81f-007c-4424-959c-23bea89f1460"
    # model_id = "8b91aa0f-b8e2-41d4-98fc-11ca80fb8a57"
    model_id = "08b1c63d-165e-40ad-b636-adb200fdb6aa"
    post_url = endpoint + "/formrecognizer/v2.0/custom/models/%s/analyze" % model_id
    params = {
        "includeTextDetails": True
    }

    headers = {
        # Request headers
        'Content-Type': file_type,
        'Ocp-Apim-Subscription-Key': apim_key,
    }
    try:
        with open(input_file, "rb") as f:
            data_bytes = f.read()
    except IOError:
        print("Inputfile not accessible.")
        sys.exit(2)

    try:
        print('Initiating analysis...')
        resp = post(url = post_url, data = data_bytes, headers = headers, params = params)
        if resp.status_code != 202:
            print("POST analyze failed:\n%s" % json.dumps(resp.json()))
            quit()
        print("POST analyze succeeded:\n%s" % resp.headers)
        print()
        get_url = resp.headers["operation-location"]
    except Exception as e:
        print("POST analyze failed:\n%s" % str(e))
        quit()

    n_tries = 15
    n_try = 0
    wait_sec = 5
    max_wait_sec = 60
    print()
    print('Getting analysis results...')
    while n_try < n_tries:
        try:
            resp = get(url = get_url, headers = {"Ocp-Apim-Subscription-Key": apim_key})
            resp_json = resp.json()
            # print("Hey {}".format(resp_json))
            # print("IF dictionary then {}".format(resp_json['analyzeResult']['documentResults'][0]['fields']['Date']['valueString']))
            if resp.status_code != 200:
                print("GET analyze results failed:\n%s" % json.dumps(resp_json))
                quit()
            status = resp_json["status"]
            if status == "succeeded":
                
                address = resp_json['analyzeResult']['documentResults'][0]['fields']['Address']['valueString']
                ifsCode = re.split('IFS Code:', address)[1]
                dateVal = resp_json['analyzeResult']['documentResults'][0]['fields']['Date']['valueString']
                payee = resp_json['analyzeResult']['documentResults'][0]['fields']['Payee']['valueString']
                amountWords = resp_json['analyzeResult']['documentResults'][0]['fields']['AmountWords']['valueString']
                amountNumbers = resp_json['analyzeResult']['documentResults'][0]['fields']['AmountNumbers']['valueString']
                micr = resp_json['analyzeResult']['documentResults'][0]['fields']['Micr']['valueString']
                # print(address)
                # print(ifsCode)
                # print(date)
                # print(payee)
                # print(amountWords)
                # print(amountNumbers)
                print(micr)
                getValidation = validation(ifsCode, dateVal, payee, amountWords, amountNumbers, micr)

                if output_file:
                    with open(output_file, 'w') as outfile:
                        json.dump(resp_json, outfile, indent=2, sort_keys=True)
                # print("Analysis succeeded:\n%s" % json.dumps(resp_json, indent=2, sort_keys=True))
                return getValidation
            if status == "failed":
                print("Analysis failed:\n%s" % json.dumps(resp_json))
                quit()
            # Analysis still running. Wait and retry.
            time.sleep(wait_sec)
            n_try += 1
            wait_sec = min(2*wait_sec, max_wait_sec)     
        except Exception as e:
            msg = "GET analyze results failed:\n%s" % str(e)
            print(msg)
            quit()
    print("Analyze operation did not complete within the allocated time.")
    # ifsCode = date = payee = amountWords = amountNumbers = micr = 0
    # getValidation = validation(ifsCode, date, payee, amountWords, amountNumbers, micr)
    return getValidation

def getArguments(argv):
    input_file = ''
    file_type = ''
    output_file = ''    
    try:
        opts, args = getopt.gnu_getopt(argv, "ht:o:", [])
    except getopt.GetoptError:
        printCommandDescription(2)

    for opt, arg in opts:
        if opt == '-h':
            printCommandDescription()

    if len(args) != 1:
        printCommandDescription()
    else:
        input_file = args[0]
    
    for opt, arg in opts:
        if opt == '-t':
            if arg not in ('application/pdf', 'image/jpeg', 'image/png', 'image/tiff'):
                print('Type ' + file_type + ' not supported')
                sys.exit()
            else:
                file_type = arg
        
        if opt == '-o':
            output_file = arg
            try:
                open(output_file, 'a')
            except IOError:
                print("Output file not creatable")
                sys.exit(2)

    if not file_type:   
        file_type = inferrType(input_file)

    return (input_file, output_file, file_type)

def inferrType(input_file):
    filename, file_extension = os.path.splitext(input_file)
    if file_extension ==  '': 
        print('File extension could not be inferred from inputfile. Provide type as an argument.')
        sys.exit()    
    elif file_extension == '.pdf':
        return 'application/pdf'
    elif file_extension ==  '.jpeg':
        return 'image/jpeg'
    elif file_extension ==  '.png':
        return 'image/png'
    elif file_extension ==  '.tiff':
        return 'image/tiff'
    else:
        print('File extension ' + file_extension + ' not supported')
        sys.exit()

def printCommandDescription(exit_status=0):
    print('analyze.py <inputfile> [-t <type>] [-o <outputfile>]')
    # print
    print('If type option is not provided, type will be inferred from file extension.')
    sys.exit(exit_status)

# if __name__ == '__main__':
    # entrymain(sys.argv[1:])
