from datetime import datetime

from ..models import Form


def setBaseForm(user, description, domains, fee_amount):
    res = False
    userId = user.id
    fid = None
    date = None
    form_status = True
    fee_amount = int(fee_amount)

    d = datetime.now()

    # Generating date
    date = str(d.month) + "/" + str(d.year)

    # Generating fid
    fid = str(userId) + d.strftime("%Y%m%d%H%M%S%f")

    try:
        form = Form(uid=user, fid=fid, date=date, description=description,
                    domains=domains, form_status=form_status, fee_amount=fee_amount)
        form.save()
        res = True
    except:
        print("!!!!!!!!!!!")
        print("Error in creating Form")

    return res


def toogleUrlStatus(fid):
    form = Form.objects.get(fid=fid)
    form.form_status = not form.form_status
    form.save()


def deleteForm(fid):
    res = False
    try:
        form = Form.objects.get(fid=fid)
        form.delete()
        res = True
    except Exception as e:
        print(">>>>>>>>>>>>>>>>Error In Deleting Form")
        print(e)

    return res
