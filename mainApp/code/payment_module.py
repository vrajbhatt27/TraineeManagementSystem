from ..models import Form
from .hashid_utils import decrypt


def getPaymentDetails(fid):
    try:
        form = Form.objects.get(fid=decrypt(fid))

        data = {
            'company': form.uid,
            'fee_amount': form.fee_amount,
            'fid': fid,
        }
    except:
        print("!!!!!!!!!!!!!!---Form Doesn't exist")
        data = {}

    return data
