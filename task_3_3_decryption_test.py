import base64
import hashlib

# TODO: key reconstruction
key = "%s" % (191443060839673982328770683981835364563 * 102110702484631269590344006605651168194)
sha512_key = hashlib.sha512(key).hexdigest()

# decode base64 message, so it is the enrypcted message
base64_message = "dg5eB08ZLFNAFBEFBQgQT1pERkRSXAgTCwERQl0EGBFQQxBOWkBTRQtREU0OE0BFcRZZXFYeFARfFlhdEls="
encrypted_message = base64.b64decode(base64_message)

# decrypt message
raw_message = ""
for i in xrange(len(encrypted_message)):
    # make XOR operation on byte from encrypted data and sha512 key
    b = ord(encrypted_message[i]) ^ ord(sha512_key[i])
    # build char out of byte and append it to decrypted string
    raw_message += chr(b)
print raw_message