from hashids import Hashids

def encrypt(fid):
    fid = int(fid)
    hid = Hashids()
    return hid.encode(fid)

def decrypt(furl):
    hid = Hashids()
    return hid.decode(furl)[0]