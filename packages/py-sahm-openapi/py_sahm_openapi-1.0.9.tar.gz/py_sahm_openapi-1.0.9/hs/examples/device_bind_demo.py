from hs.bind.device_bind import bind

# 开发者RSA私钥。和直接私钥对应的公钥，需要填写到平台，给平台加密使用
ENCRYPT_RSA_PRIVATEKEY = """MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBALAeGxs3kBu7oTAr
F 8 Lwr AIZ Y fH S Aru O QO/lLZC3cbXWp0Hv0q1pra6UBACb8DHTprr3i182N9qwPf3l
rDRb3K41luoFCF+V6jkDwjaZU0e0m/5sMRQDKoiZP7YRyh8BGKoX5B/p 9 J xB 6 Cw n
7FrFt01qEIoL6LxfUL1q6abSjg07AgMBAAECgYAIr3NmxDa3J2mrlnR1iKjy8Y2C
/3hjB4DsU8ELggB5lzxoZAtfwfZuxZ3s6cPOsUFntw2IhIP8pPRpsQntCxq257wd
iyUT4iVE8D20lIWRB32bsN5gH2jtsv7ieUT6UpM4jllxTPqw26gbNrFc+G8kqOb2
E5aX4HcmdhruY9yEAQJBANWTPRKE9VgxAFVm3pB8lDl17G9ufQ8DIJlp6wRncmOD
G6dOwziyLkp5yWjVxT3h0P+GaO5c0dthjfvwZZy3YQsCQQDTGhHCJbW1ZQRIwuH/
KeesrrCGGfTpTGNAvUffK+UMCUTPeYI0HJTAOeGTAL/X+7xpnnzLbyBziUAgSgHw
igKRAkBVSzkftUO6Vc95S9zkvSwBCqxDEFAXd7tEKX23Q4z2WvznQ1hJwzcjfSHH
OV/lR9LMyaQMVbtlrr8id65M+RtjAkEAkbJ8bzL3pqqBunZG5IVXkKdAzk0764j9
N8FryWvSOexrwYZrhuvy/nj0ZzEtNzRXZc4s83tPOm6QA7kQfaPDAQJAUuwBFWWj
SbksHBaHrRGMhyxDvse7ujfaSIjugriO8ew1BNFFBhrTq8Y41W6Ptq+wvp1K8/yh
V8kn+I5fs2ZDRw=="""


def format_rsa_private_key(orginal_key: str):
    return "".join(line.strip() for line in orginal_key.splitlines())


def start_bind_test():
    print(f"Developer private key used for test environment:{format_rsa_private_key(ENCRYPT_RSA_PRIVATEKEY)}")
    bind()


if __name__ == '__main__':
    start_bind_test()
