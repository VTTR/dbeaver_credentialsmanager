import base64

PASSWORD_ENCRYPTION_KEY = b"sdf@!#$verf^wv%6Fwe%$$#FFGwfsdefwfe135s$^H)dg"


def encrypt(newpass: str) -> str:
    ba : bytearray = bytearray(len(newpass) + 2)

    for index, _ in enumerate(newpass):
        ba[index] = ord(newpass[index])

    ba[-1] = 129
    ba[-2] = 0

    output = bytearray(b"")
    for i in range(len(ba)):
        output.append(ba[i] ^ PASSWORD_ENCRYPTION_KEY[i % len(PASSWORD_ENCRYPTION_KEY)])
    return base64.b64encode(output).decode('utf-8')


def decrypt(password: str) -> str:
    data_bin = base64.b64decode(password)
    output = bytearray(b"")

    for i in range(len(data_bin)):
        output.append(data_bin[i] ^ PASSWORD_ENCRYPTION_KEY[i % len(PASSWORD_ENCRYPTION_KEY)])

    return output[:-2].decode('utf-8')
