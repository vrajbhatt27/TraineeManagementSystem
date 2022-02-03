from ..models import Form, Trainee
from .hashid_utils import encrypt, decrypt


def getDataForTform(fid):
    try:
        form = Form.objects.get(fid=decrypt(fid))
        if form.form_status == False:
            return -1

        domain_lst = form.domains.split('\r\n')
        data = {
            'description': form.description,
            'domains': domain_lst,
            'company': form.uid,
            'fid': fid,
        }
    except:
        print("!!!!!!!!!!!!!!---Form Doesn't exist")
        data = {}

    return data


def saveDataForTform(fid, trainee_name, trainee_email, trainee_age, trainee_college, trainee_cgpa, trainee_hsc, trainee_ssc, trainee_domain):
    res = False

    if Trainee.objects.filter(trainee_email=trainee_email, fid=decrypt(fid)).exists():
        return -1

    try:
        fid = decrypt(fid)
        trainee = Trainee(fid=fid, trainee_name=trainee_name, trainee_email=trainee_email, trainee_college=trainee_college,
                          trainee_age=trainee_age, trainee_cgpa=trainee_cgpa, trainee_hsc=trainee_hsc, trainee_ssc=trainee_ssc, trainee_domain=trainee_domain)

        trainee.save()
        res = True
    except Exception as e:
        print("------------------------")
        print(e)
        print("Can't save trainee !!!")

    return res
