from hashids import Hashids

def encrypt(fid):
    fid = int(fid)
    hid = Hashids()
    return hid.encode(fid)

def decrypt(furl):
    hid = Hashids()
    return hid.decode(furl)[0]


x = encrypt('220220131172524031641')
print(type(x))
print("---")
print(decrypt(x))