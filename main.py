# This file saves form responses from typeform.com into a CSV file with a title
# row composed of questions
# ***** *** * *** ****** 
# Created by Singh 2017

import requests, csv

api = "XXXX"
formNumb = 0 # Select which form to get data from, default 0 for first form

# Get all forms via api key and retrieve form UIDs
r = requests.get('https://api.typeform.com/v1/forms?key=' + api)

if (r.status_code == 200) :
    #print r.json() # display list of forms
    typeform_UID = r.json()[formNumb]["id"]
    if (typeform_UID != '') :

        # Get form data and store in variables so no need to requery again
        r2 = requests.get('https://api.typeform.com/v1/form/' + 
                            typeform_UID + '?key=' + api)
        if (r2.status_code == 200) :
            questionsData = r2.json()['questions']
            responsesData = r2.json()['responses']

            # create array of question ids to map for column CSV display 
            questionIDs = [] 
            questionsTitleRow = [] # prepare title first row with questions for CSV export
            responsesRow = [] # each row is each seperate submission

            for id in questionsData:
                questionIDs.append(id["id"])
                questionsTitleRow.append((id["question"]).encode('utf-8'))
            
            ##print questionIDs
            # get answers with order from questionIDs
            x = []
            for answers in responsesData:
                ##print answers['answers']
                x = [] # empty x
                for eachId in questionIDs:
                    try:
                        x.append(str(answers['answers'][eachId]))
                    except:
                        x.append('')
                ##print (x)
                responsesRow.append(x)

        else :
            print "error - in typeform UID request"

    else :
        print ("error - typeform UID not found")

else :
    print "No response please check api key"

# Save data to csv
fileName = "import-me.csv"
f = open(fileName, "wb")
writer = csv.writer(f, delimiter=',',)
titleString = ""
for questions in questionsTitleRow:
    titleString += "'" + questions + "',"
writer.writerow(questionsTitleRow)

for responses in responsesRow:
    writer.writerow(responses)

f.close()
print "done"
