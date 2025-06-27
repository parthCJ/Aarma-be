import os

CA_PATH   = "../certs/AmazonRootCA1.pem"
CERT_PATH = "../certs/8805dbe759dbb5b938494f05b7c2712546d9ef678ba719f4cf40f330b4d290de-certificate.pem.crt"
KEY_PATH  = "../certs/8805dbe759dbb5b938494f05b7c2712546d9ef678ba719f4cf40f330b4d290de-private.pem.key"

print("CA exists:   ", os.path.exists(CA_PATH))
print("CERT exists: ", os.path.exists(CERT_PATH))
print("KEY exists:  ", os.path.exists(KEY_PATH))
