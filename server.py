import sys

from flask import Flask, send_from_directory, jsonify, request, render_template

from random import randint

app = Flask(__name__, static_folder='views')


# - - - - - - - - - - - - - - - - 
# ** Offset **
# This algorithm encrypts a message by getting a character's ASCII code, offestting it by a set amount, and returning the ASCII character that corresponds to the new number.
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
# ** Shared Key **
# This algorithm encrypts a message by getting a character's ASCII code, offsetting it by the ASCII code of a character in the key. Each character in the message is offset by the ASCII code of the next character in they key. If the message is longer than the key the ASCII codes from the key are repeated. 
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
# **  Public Key **
# This algorithm encrypts a message by using public keys generated on the front end. The ASCII code of each character in the message is converted into a number using the public key. To decrypt the message, the number is converted back into an ASCII code using the private key.
# - - - - - - - - - - - - - - - - 
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def coprime(a, b):
    return gcd(a, b) == 1
  

def publicKeyEncrypt(plaintext_message, public_keys):
  newString = ""
  count = 0
  messageLength = len(plaintext_message)
  for c in plaintext_message:
    intC = ord(c)
    newIntC = ((intC**public_keys[0]) % public_keys[1])
    newString += str(newIntC)
    count += 1
    if count >= messageLength:
      pass
    else:
      newString += ", "
  return newString
  
def publicKeyDecrypt(encrypted_message, private_keys):
  encrypted_array = []
  decrypted_string = ""
  count = 0
  placeholder_string = ""
  for c in encrypted_message:
    if c != "," and c !=" ":
      placeholder_string += c
    else:
      if c == ",":
        encrypted_array.append(int(placeholder_string))
        placeholder_string = ""
      else:
        pass
  encrypted_array.append(int(placeholder_string))
  
  for i in encrypted_array:
    decrypted_int = (i**private_keys[0] % private_keys[1])
    decrypted_string += chr(decrypted_int)
  return decrypted_string

# - - - - - - - - - - - - - - - - 
# Routes
# - - - - - - - - - - - - - - - - 

@app.route("/")
def hello():
  return render_template('index.html')

# Offset:

@app.route("/offset/encrypt", strict_slashes=False)
def offset_encrypt():
  message = request.args.get("message")
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
    return render_template("offset.html")

@app.route("/offset/decrypt", strict_slashes=False)
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
    return render_template("offset.html")

@app.route("/offset", strict_slashes=False)
def offset():
  return render_template("offset.html")

# Shared Key:

@app.route("/shared-key/encrypt", strict_slashes=False)
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
    return render_template("shared-key.html")
  
@app.route("/shared-key/decrypt", strict_slashes=False)
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
    return render_template("shared-key.html")

@app.route("/shared-key", strict_slashes=False)
def shared_key():
  return render_template("shared-key.html")

# Public Key:

@app.route("/public-key/primes", strict_slashes=False)
def available_coprimes():
  prime1 = int(request.args.get("prime1"))
  prime2 = int(request.args.get("prime2"))
  largerPrime = prime1
  if (prime1 - prime2) < 0:
    largerPrime = prime2
  modulus = prime1 * prime2
  coprimesOf = (prime1 - 1) * (prime2 - 1)
  coprimes = []
  for n in range(largerPrime + 2, coprimesOf):
    if coprime(n, coprimesOf):
      coprimes.append(n)
  return jsonify(coprimes)

@app.route("/public-key/keys", strict_slashes=False)
def keys():
  prime1 = int(request.args.get("prime1"))
  prime2 = int(request.args.get("prime2"))
  coprime = int(request.args.get("coprime"))
  modulus = prime1 * prime2
  coprimesOf = (prime1 - 1) * (prime2 - 1)
  encryptExponent = coprime
  decryptExponent = 0
  publicKeys = [encryptExponent, modulus]
  for n in range(2, coprimesOf):
    if (n * encryptExponent) % coprimesOf == 1:
      decryptExponent = n
      privateKeys = [decryptExponent, modulus]
      if publicKeys == privateKeys:
        return jsonify({"error": "Private and public key were the same, use different numbers"})
      else:
        return jsonify({"publicKeys": publicKeys, "privateKeys": privateKeys})
  if decryptExponent  == 0:
    return jsonify(["Error", "No private decrypt exponent found."])
  return jsonify(["Error", "Ended without valid return"])

@app.route("/public-key/encrypt", strict_slashes=False)
def public_key_encrypt():
  publicKey = []
  publicKey.append(int(request.args.get("public-key-1")))
  publicKey.append(int(request.args.get("public-key-2")))
  message = request.args.get("message")
  if publicKey and message:
    return render_template(
    "public-key-encrypt-message.html",
    public_keys = publicKey,
    message = message,
    encrypted_message = publicKeyEncrypt(message, publicKey)
    )
  else:
    return render_template("public-key.html")
  

@app.route("/public-key/decrypt", strict_slashes=False)
def public_key_decrypt():
  privateKeys = []
  privateKeys.append(int(request.args.get("private-key-1")))
  privateKeys.append(int(request.args.get("private-key-2")))
  message = request.args.get("message")
  if privateKeys and message:
    return render_template(
    "public-key-decrypt-message.html",
    private_keys = privateKeys,
    encrypted_message = message,
    decrypted_message = publicKeyDecrypt(message, privateKeys)
    )
  return

@app.route("/public-key", strict_slashes=False)
def public_key():
  return render_template("public-key.html")

# Public Directory:

@app.route('/<path:path>', strict_slashes=False)
def send_static(path):
  return send_from_directory('public', path)

if __name__ == "__main__":
  app.run()
