from datetime import datetime
import json
from ..models import Form, Test, Trainee
import csv
from .hashid_utils import encrypt, decrypt


def createTest(user, description, domain, file):
    res = False
    userId = user.id
    test_status = True
    questions = {}

    # Generating test_id:
    d = datetime.now()
    test_id = str(userId) + d.strftime("%Y%m%d%H%M%S%f")

    # creating map from csv file:
    file = file.read().decode().splitlines()
    reader = csv.reader(file)

    for index, row in enumerate(reader, 1):
        questions['q' + str(index)] = {
            'question': row[0],
            'op1': row[1],
            'op2': row[2],
            'op3': row[3],
            'op4': row[4],
            'ans': row[5]
        }

    json_data = json.dumps(questions)
    # Saving Data
    try:
        test = Test(uid=user, test_id=test_id,
                    domain=domain, description=description, questions=json_data, test_status=test_status)
        test.save()
        res = True
    except Exception as e:
        print("!!!!!!!!!!!")
        print("Error in creating Form", e)

    return res

# Get all questions for test form:


def getData(tid):
    try:
        test = Test.objects.get(test_id=decrypt(tid))
        if test.test_status == False:
            return -1

        data = {
            'domain': test.domain,
            'description': test.description,
            'questions': json.loads(test.questions)
        }
    except Exception as e:
        print("!!!!!!!!!!!!!!---Form Doesn't exist", e)
        data = {}

    return data


def getKeys(tid):
    try:
        test = Test.objects.get(test_id=decrypt(tid))

        data = {}
        data = json.loads(test.questions)
        data = list(data.keys())
    except Exception as e:
        print("!!!!!!!!!!!!!!---Form Doesn't exist", e)
        data = {}

    return data

# Score and other processes


def saveData(email, ans, tid):
    res = False
    questions = getData(tid)
    questions = questions['questions']
    if questions == -1 or len(questions) == 0:
        return -1

    score = 0
    # Checking the score
    for i in range(len(questions)):
        key = 'q' + str(i+1)
        if questions[key]['ans'] == ans[i]:
            score += 1

    # generating date:
    d = datetime.now()
    date = str(d.month) + "/" + str(d.year)

    # Adding score to database
    try:
        fid = (Form.objects.get(date=date)).fid
        trainee = Trainee.objects.get(trainee_email=email, fid=fid)
        if trainee.trainee_score != None:
            return -1

        trainee.trainee_score = score
        trainee.save()

        res = True
    except Exception as e:
        print("--Something went wrong while subitting the test", e)

    return res


# Filter Trainee

def filterTrainee(score):
    try:
        trainee_list = Trainee.objects.filter(trainee_score__lt=score)
        for trainee in trainee_list:
            trainee.delete()

    except Exception as e:
        print("Error in deleting trainee", e)

# Toogle Test Status:


def toogleTestStatus(tid):
    test = Test.objects.get(test_id=tid)
    test.test_status = not test.test_status
    test.save()

# Delete Test:


def deleteTest(tid):
    res = False
    try:
        test = Test.objects.get(test_id=tid)
        test.delete()
        res = True
    except Exception as e:
        print(">>>>>>>>>>>>>>>>Error In Deleting Form")
        print(e)

    return res
