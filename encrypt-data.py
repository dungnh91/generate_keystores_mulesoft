#!/usr/bin/python3

import sys
# necessary imports
import secrets
import string
import subprocess
import re

pwd_length = sys.argv[1]
print("password length: " + pwd_length)
pwd_length = int(pwd_length)

# generate password meeting constraints
def generate_password(length = pwd_length):
    # define the alphabet
    letters = string.ascii_letters
    digits = string.digits
    # special_chars = string.punctuation
    special_chars = "@#$%^&*()<>?,./|[]-=_+~`{}"

    alphabet = letters + digits + special_chars

    while True:
        pwd = ''
        for i in range(length):
            pwd += ''.join(secrets.choice(alphabet))

        if (sum(char in special_chars for char in pwd)>=10 and 
            sum(char in digits for char in pwd)>=9):
                break
    return pwd

def clean_keystores():
    print ("Cleaning keystores .......")
    subprocess.call("rm -rf keystores && rm -rf *.jks")
    subprocess.call("mkdir keystores")

def generate_keystore(env, pwd):
    print ("Generating keystore for {} .......".format(env.upper()))    
    subprocess.call('keytool -v -genkeypair -keyalg RSA -dname "CN=DUNG NGUYEN, OU=BYCN IT, O=BYCN, L=HCMC, ST=HCM, C=VN" -validity 365 -storetype PKCS12 -keystore {}.jks -alias {} -storepass {}'.format(env, env, pwd))
    subprocess.call("mv {}.jks keystores/".format(env))
    with open("keystores/pwd.txt", 'a') as file:
        file.write("{}:\t{}\n".format(env.upper(), pwd))

def generate_mule_key():
    print ("Generate key for mulesoft")
    key = generate_password(32)
    with open("keystores/key.txt", 'w') as file:
        file.write(key)
    print ("Generating passwords .......")
    for env in envs:
        print ("Generate password for {}".format(env.upper()))
        pwd = generate_password()
        while len(encrypted_pwd:= encrypt_password(key, pwd)) == 0 :
            pwd = generate_password()
        with open("keystores/pwd_encrypted.txt", 'a') as file:
            file.write("{}:\t{}\n".format(env.upper(), encrypted_pwd))
        generate_keystore(env, pwd)

    return key

def encrypt_password(key, pwd):
    if len(pwd) == 0:
        return ""
    encrypted_pwd = subprocess.check_output('java -cp secure-properties-tool.jar com.mulesoft.tools.SecurePropertiesTool string encrypt AES CBC "{}" "{}"'.format(key, pwd), text=True).rstrip()
    # print ('java -cp secure-properties-tool.jar com.mulesoft.tools.SecurePropertiesTool string decrypt AES CBC "{}" "{}"'.format(key, temp))
    plain_pwd = subprocess.check_output('java -cp secure-properties-tool.jar com.mulesoft.tools.SecurePropertiesTool string decrypt AES CBC "{}" "{}"'.format(key, encrypted_pwd), text=True).rstrip()
    if(pwd != plain_pwd):
        print(pwd)
    return encrypted_pwd

# def encrypt_password(key, pwd):
#     with open("keystores/pwd_encrypted.txt", 'a') as file:
        
# def encrypt_password(key, pwd):
#     key = generate_mule_key()
#     print ("Encrypting passwords .......")
#     envs_string = ("|".join(envs)).upper()
#     print(envs_string)
#     with open("keystores/pwd.txt") as file:
#         for line in file.readlines():            
#             pwd = re.sub("({}):\s*".format(envs_string), "", line)
#             print('java -cp secure-properties-tool.jar com.mulesoft.tools.SecurePropertiesTool string encrypt AES CBC "{}" "{}"'.format(key, pwd))
#             encrypted_pwd = subprocess.call('java -cp secure-properties-tool.jar com.mulesoft.tools.SecurePropertiesTool string encrypt AES CBC "{}" "{}"'.format(key, pwd))
#             print (encrypted_pwd)
#             with open("keystores/pwd_encrypted.txt", 'a') as file:
#                 file.write("{}:\t{}\n".format(env.upper(), encrypted_pwd))
#     return ""


clean_keystores()

envs = ["dev", "rec", "prod"]
# for env in envs:
#     generate_keystores(env)

# print ("Finished generating keystores")

# encrypt_passwords()
generate_mule_key()
