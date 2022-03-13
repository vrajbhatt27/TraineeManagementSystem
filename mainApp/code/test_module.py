from datetime import datetime
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
