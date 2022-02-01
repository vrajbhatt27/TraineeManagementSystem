from ..models import Form, Trainee

def getTraineeData(fid):
    data = []
    try:
        trainee_list = Trainee.objects.filter(fid=fid)
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
            })
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!>", "Can't get form data")
        print(e)
    
    return data
        