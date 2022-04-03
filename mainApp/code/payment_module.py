from ..models import Form, Trainee
from .hashid_utils import decrypt
from django.conf import settings


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


def setUpPayment(fid, email, razorpay_client):
    data = getPaymentDetails(fid)
    try:
        trainee = Trainee.objects.get(fid=decrypt(fid), trainee_email=email)
    except:
        print("!!!!!!!!!!!!!!---Form Doesn't exist")
        return -1

    # Setup for razorpay
    try:
        amount = data['fee_amount']*100

        DATA = {
            "amount": amount,
            "currency": "INR",
        }

        payment = razorpay_client.order.create(data=DATA)

        data["order_id"] = payment['id']
        data["amount"] = amount
        data["key_id"] = settings.RAZORPAY_KEY_ID
        data["callback_url"] = 'http://127.0.0.1:8000/tms/makePayment/paymentHandler/'
        data["name"] = trainee.trainee_name
        data["email"] = trainee.trainee_email
        data["ok"] = True
    except Exception as e:
        print(e)
        return -1

    # change payment_id in trainee table
    trainee.trainee_paymentId = payment["id"]
    trainee.save()

    return data


"""
def handlePayment(payment_id, razorpay_order_id, signature):
    res = False
    try:
        razorpay_client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        # verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(
            params_dict)

        if result:
            trainee = Trainee.objects.get(trainee_paymentId=razorpay_order_id)
            print("-----------------")
            print(trainee)
            trainee.trainee_paymentStatus = True
            trainee.save()
            res = True
        else:
            res = False
    except Exception as e:
        res = False
        print(e)

    return res
"""


def savePaymentStatus(order_id):
    res = False
    try:
        trainee = Trainee.objects.get(trainee_paymentId=order_id)
        trainee.trainee_paymentStatus = True
        trainee.save()
        res = True
    except:
        print("Can't Find Trainee !!!--------------")

    return res
