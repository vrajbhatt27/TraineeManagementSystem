from ..models import Form, Trainee


def getTraineeData(fid, domain=''):
    data = []
    try:
        if domain == '':
            trainee_list = Trainee.objects.filter(fid=fid)
        else:
            trainee_list = Trainee.objects.filter(
                fid=fid, trainee_domain=domain)

        for t in trainee_list:
            data.append({
                'tname': t.trainee_name,
                'temail': t.trainee_email,
                'tage': t.trainee_age,
                'tcollege': t.trainee_college,
                'tcgpa': t.trainee_cgpa,
                'thsc': t.trainee_hsc,
                'tssc': t.trainee_ssc,
                'tdomain': t.trainee_domain,
                'tresume': t.trainee_resume,
                'tscore': t.trainee_score,
                'tpaymentStatus': t.trainee_paymentStatus,
            })
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!>", "Can't get trainee data")
        print(e)

    return data


def getFormData(fid):
    data = []
    try:
        form = Form.objects.filter(fid=fid)

        for f in form:
            data.append({
                'description': f.description,
                'date': f.date,
                'domains': f.domains,
            })
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!>", "Can't get form data")
        print(e)

    if ' ' in data[0]['domains']:
        data[0]['domains'] = data[0]['domains'].replace(' ', '-')

    domains = data[0]['domains'].split('\r\n')
    data[0]['domains'] = domains

    return data[0]


def delete_trainee(temail, fid):
    res = False
    try:
        trainee = Trainee.objects.get(trainee_email=temail, fid=fid)
        trainee.delete()
        res = True
    except Exception as e:
        print(">>>>>>>>>>>>>>>>Error In Deleting")
        print(e)

    return res

# Filter Trainee


def filterTrainee(fid, score=0, payment=False):
    try:
        if payment:
            trainee_list = Trainee.objects.filter(
                fid=fid, trainee_paymentStatus=False)
        else:
            trainee_list = Trainee.objects.filter(
                fid=fid, trainee_score__lt=score)

        for trainee in trainee_list:
            trainee.delete()

    except Exception as e:
        print("Error in deleting trainee", e)
