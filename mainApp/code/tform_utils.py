from ..models import Form

def getDataForTform(fid):
    try:
        form = Form.objects.get(fid=fid)
        domain_lst = form.domains.split('\r\n')
        data = {
            'description': form.description,
            'domains': domain_lst,
            'company': form.uid,
        }
    except:
        print("!!!!!!!!!!!!!!---Form Doesn't exist")
        data = {}
    
    return data