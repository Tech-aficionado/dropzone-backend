from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])
print(
    pwd_context.verify(
        "qazPLM123", "$2b$12$xVD/ZecY20HcpvRhdCFka.T/hPsd6vlOrukdDSmRfwHU8SWC1xJGG"
    )
)
print(pwd_context.to_string('$2b$12$xVD/ZecY20HcpvRhdCFka.T/hPsd6vlOrukdDSmRfwHU8SWC1xJGG'))
# print(pwd_context.hash('string',))
