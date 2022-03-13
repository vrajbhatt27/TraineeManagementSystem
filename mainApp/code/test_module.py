from datetime import datetime
import json
from ..models import Test
import csv


def createTest(user, description, domain, file):
    res = False
    userId = user.id
    test_status = True
    questions = []

    # Generating test_id:
    d = datetime.now()
    test_id = str(userId) + d.strftime("%Y%m%d%H%M%S%f")

    # creating map from csv file:
    file = file.read().decode().splitlines()
    reader = csv.reader(file)

    for row in reader:
        questions.append({
            'question': row[0],
            'op1': row[1],
            'op2': row[2],
            'op3': row[3],
            'op4': row[4],
            'ans': row[5]
        })

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
