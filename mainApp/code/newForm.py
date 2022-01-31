from datetime import datetime

from ..models import Form

def setBaseForm(user, description, domains):
    res = False
    userId = user.id
    fid = None
    date = None
    form_status = True

    d = datetime.now()

    # Generating date
    date = str(d.month) + "/" + str(d.year)

    # Generating fid
    fid = str(userId) + d.strftime("%Y%m%d%H%M%S%f")

    try:
        form = Form(uid=user, fid=fid, date=date, description=description,
                    domains=domains, form_status=form_status)
        form.save()
        res = True
    except:
        print("!!!!!!!!!!!")
        print("Error in creating Form")

    return res
    