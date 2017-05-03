import sys

from flask import Flask, send_from_directory, jsonify, request, render_template
app = Flask(__name__, static_folder='views')


# - - - - - - - - - - - - - - - - 
# Offset
# - - - - - - - - - - - - - - - - 

def offsetEncrypt(myString, myOffset):
  newString = ""
  intOffset = int(myOffset)
  for c in myString:
    intC = ord(c)
    if intC > 126:
      return "Error"
    if intC < 32:
      return "Error"
    newIntC = intC + intOffset
    if newIntC > 126:
      newIntC = newIntC - 95
    newChar = chr(newIntC)
    newString += newChar
  return newString
  
def offsetDecrypt(myEncodedString, myOffset):
  newString = ""
  intOffset = int(myOffset)
  for c in myEncodedString:
    intC = ord(c)
    if intC > 126:
      return "Error"
    if intC < 32:
      return "Error"
    newIntC = intC - intOffset
    if newIntC < 32:
      newIntC = newIntC + 95
    newChar = chr(newIntC)
    newString += newChar
  return newString

# - - - - - - - - - - - - - - - - 
# Shared Key
# - - - - - - - - - - - - - - - - 

def keyEncrypt(myString, myPassword):
  newString = ""
  for c in myPassword:
    if ord(c) > 126:
      return "Error"
  count = 0
  passwordLength = len(myPassword)
  for c in myString:
    intC = ord(c)
    if intC > 126:
      return "Error"
    if intC < 32:
      return "Error"
    offset = ord(myPassword[count])
    newIntC = intC + offset
    if newIntC > 126:
      newIntC = newIntC - 95
      if newIntC > 126:
        newIntC = newIntC - 95
    newChar = chr(newIntC)
    newString += newChar
    
    count += 1
    if count == passwordLength:
      count = 0
  return newString

def keyDecrypt(myEncodedString, myPassword):
  newString = ""
  for c in myPassword:
    if ord(c) > 126:
      return "Error"
  count = 0
  passwordLength = len(myPassword)
  for c in myEncodedString:
    intC = ord(c)
    if intC > 126:
      return "Error"
    if intC < 32:
      return "Error"
    offset = ord(myPassword[count])
    newIntC = intC - offset
    if newIntC < 32:
      newIntC = newIntC + 95
      if newIntC < 32:
        newIntC = newIntC + 95
    newChar = chr(newIntC)
    newString += newChar
    
    count += 1
    if count == passwordLength:
      count = 0
  return newString

# - - - - - - - - - - - - - - - - 
# Public Key
# - - - - - - - - - - - - - - - - 

from random import randint

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def coprime(a, b):
    return gcd(a, b) == 1
  
primesUnder20 = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

def generateKeys():
  
  print("Pick one of the following prime numbers:")
  for p in primesUnder20:
    print(p)
  print()
  prime1 = int(input())
  if prime1 not in primesUnder20:
    return ["Error", "Not a valid prime number."]
  print("-- Prime 1: " + str(prime1))
  print()
  
  print("Pick another of the following prime numbers:")
  for p in primesUnder20:
    if p != prime1:
      if p != prime1 - 1:
        if p != prime1 + 1:
          print(p)
  print()
  prime2 = int(input())
  if prime2 not in primesUnder20:
    return ["Error", "Not a valid prime number."]
  if prime2 == prime1:
    return ["Error", "Primes chosen are the same"]
  print("-- Prime 2: " + str(prime2))
  print()
  
  modulus = prime1 * prime2
  coprimesOf = (prime1 - 1) * (prime2 - 1)
  print("-- Modulus: " + str(modulus))
  
  print()
  print("Pick one of the following coprimes with " + str(coprimesOf) + " [(" + str(prime1) + " - 1) * (" + str(prime2) + " - 1)]:")
  validEEs = []
  for n in range(2, coprimesOf):
    if coprime(n, coprimesOf):
      validEEs.append(n)
      print(n)
  print()
  print("Pick one of the above coprimes with " + str(coprimesOf) + " [(" + str(prime1) + " - 1) * (" + str(prime2) + " - 1)]:")
  print()
  ee = int(input())
  if ee in validEEs:
    print("-- Encryption Exponent: " + str(ee))
    print()
    publicKeys = [ee, modulus]
  else:
    return ["Error", "Not a valid coprime."]
  
  de = 0
  for n in range(2, coprimesOf):
    if (n * ee) % coprimesOf == 1:
      de = n
      print("-- Decrypt Exponent: " + str(de))
      privateKeys = [de, modulus]
      return [publicKeys, privateKeys]
  if de == 0:
    return ["Error", "No private decrypt exponent found."]
  return["Error", "Ended without valid return"]

def charToTildeString(tildeString, nonAsciiInt):
  if nonAsciiInt > 93:
    rand = randint(0, 93)
    tildeString += chr(rand + 32)
    nonAsciiInt = nonAsciiInt - rand
    return charToTildeString(tildeString, nonAsciiInt)
  else:
    tildeString += chr(nonAsciiInt + 32)
    tildeString += "~"
    return tildeString
  

def privateKeyEncrypt(plainMessage, key):
  newString = ""
  count = 0
  for c in plainMessage:
    intC = ord(c) - 32
    if intC > 93:
      return "Error"
    if intC < 0:
      return "Error"
    newIntC = ((intC**key[0]) % key[1])
    if newIntC > 93:
      tildeAdd = charToTildeString("~", newIntC)
      newString += tildeAdd
    else: 
      newChar = chr(newIntC + 32)
      newString += newChar
      count += 1
      if count > 93:
        count = 0
  return newString
  
def privateKeyDecrypt(encMessage, key):
  newString = ""
  tildeBank = 0
  inTilde = False
  count = 0
  for c in encMessage:
    convChar = False
    if c == "~":
      if inTilde:
        intC = tildeBank
        tildeBank = 0
        inTilde = False
        convChar = True
      else:
        inTilde = True
    else:
      if inTilde:
        tildeBank += ord(c) - 32
      else:
        intC = ord(c) - 32
        if intC > 93:
          return "Error"
        if intC < 0:
          return "Error"
        convChar = True
    if convChar:
      newIntC = ((intC**key[0]) % key[1])
      newChar = chr(newIntC + 32)
      newString += newChar
      count +=1
      if count > 93:
        count = 0
  return newString

# - - - - - - - - - - - - - - - - 
# Routes
# - - - - - - - - - - - - - - - - 

@app.route("/")
def hello():
  return app.send_static_file('index.html')

# Offset:

@app.route("/offset/encrypt")
def offset_encrypt():
  message = request.args.get("message")
  print("*********")
  print(message)
  print("*********")
  offset = request.args.get("offset")
  if message and offset:
    encrypted_message = offsetEncrypt(message, offset)
    message = offsetDecrypt(encrypted_message, offset)
    return render_template(
      "offest-encrypt-message.html",
      offset=offset,
      message=message,
      encrypted_message=encrypted_message
    )
  else: 
    return app.send_static_file("offset.html")

@app.route("/offset/decrypt")
def offset_decrypt():
  message = request.args.get("message")
  offset = request.args.get("offset")
  if message and offset:
    decrypted_message = offsetDecrypt(message, offset)
    return render_template(
      "offest-decrypt-message.html",
      offset=offset,
      message=message,
      decrypted_message=decrypted_message
    )
  else: 
    return app.send_static_file("offset.html")

@app.route("/offset")
def offset():
  return app.send_static_file("offset.html")

# Shared Key:

@app.route("/shared-key/encrypt")
def shared_key_encrypt():
  message = request.args.get("message")
  key = request.args.get("key")
  if message and key:
    encrypted_message = keyEncrypt(message, key)
    return render_template(
    "shared-key-encrypt-message.html",
    key=key,
    message=message,
    encrypted_message=encrypted_message
    )
  else:
    return app.send_static_file("offset.html")
  
@app.route("/shared-key/decrypt")
def shared_key_decrypt():
  message = request.args.get("message")
  key = request.args.get("key")
  if message and key:
    decrypted_message = keyDecrypt(message, key)
    return render_template(
    "shared-key-decrypt-message.html",
    key=key,
    message=message,
    decrypted_message=decrypted_message
    )
  else:
    return app.send_static_file("offset.html")

@app.route("/shared-key")
def shared_key():
  return app.send_static_file("shared-key.html")

# Public Key:

@app.route("/public-key")
def public_key():
  return app.send_static_file("public-key.html")

# Public Directory:

@app.route('/<path:path>')
def send_static(path):
  return send_from_directory('public', path)

if __name__ == "__main__":
  app.run()
