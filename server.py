import sys, time

from flask import Flask, send_from_directory, jsonify, request, render_template

from random import randint

app = Flask(__name__, static_folder='views')


# - - - - - - - - - - - - - - - -
# To clean input turn line breaks into spaces
# - - - - - - - - - - - - - - - -

def line_break_to_space(my_string):
  string_list = list(my_string)
  for i in range(0, len(string_list)):
    #print(str(i) + ": " + string_list[i] + " (" + str(ord(string_list[i])) + ")")
    if ord(string_list[i]) == 13:
      string_list[i] = " "
    if ord(string_list[i]) == 10:
      string_list[i] = ""
  return "".join(string_list)

# - - - - - - - - - - - - - - - -
# To find the decrypted strings with the most spaces
# - - - - - - - - - - - - - - - -

def find_spaces(my_possible_strings):
  spaces_list = []
  for i in range(0, len(my_possible_strings)):
    spaces = 0
    for c in my_possible_strings[i]:
      if ord(c) == 32:
        spaces += 1
    spaces_list.append({"spaces": spaces, "index": i})
                 
  # my_list = sorted(my_list, key=lambda k: k['name'])
  spaces_list = sorted(spaces_list, key=lambda k: k["spaces"], reverse=True)
  most_likely_indexes = [spaces_list[0]["index"], spaces_list[1]["index"], spaces_list[2]["index"]]
                 
  return most_likely_indexes


# - - - - - - - - - - - - - - - - 
# ** Offset **
# This algorithm encrypts a message by getting a character's ASCII code, offestting it by a set amount, and returning the ASCII character that corresponds to the new number.
# - - - - - - - - - - - - - - - - 

def offset_encrypt(my_string, my_offset):
  clean_string = line_break_to_space(my_string)
  new_string = ""
  int_offset = int(my_offset)
  count = 0
  for c in clean_string:
    int_c = ord(c)
    if int_c > 126:
      return "Error: Greater than 126"
    if int_c < 32:
      return "Error: Less than 32"
    new_int_c = int_c + int_offset
    if new_int_c > 126:
      new_int_c = new_int_c - 95
    new_char = chr(new_int_c)
    new_string += new_char
    count += 1
  return new_string
  
def offset_decrypt(my_encoded_string, my_offset):
  new_string = ""
  int_offset = int(my_offset)
  for c in my_encoded_string:
    int_c = ord(c)
    if int_c > 126:
      return "Error"
    if int_c < 32:
      return "Error"
    new_int_c = int_c - int_offset
    if new_int_c < 32:
      new_int_c = new_int_c + 95
    new_char = chr(new_int_c)
    new_string += new_char
  return new_string

def offset_brute_force(my_encoded_string):
  new_strings = []
  # Do the following for each offest someone might have chosen
  for possible_offset in range(1, 95):
    # Test that offset on each character of the enrypted message
    new_string = offset_decrypt(my_encoded_string, possible_offset)
    new_strings.append(new_string)
  return new_strings




# - - - - - - - - - - - - - - - - 
# ** Shared Key **
# This algorithm encrypts a message by getting a character's ASCII code, offsetting it by the ASCII code of a character in the key. Each character in the message is offset by the ASCII code of the next character in they key. If the message is longer than the key the ASCII codes from the key are repeated. 
# - - - - - - - - - - - - - - - - 

def keyEncrypt(myString, myPassword):
  clean_string = line_break_to_space(myString)
  newString = ""
  for c in myPassword:
    if ord(c) > 126:
      return "Error"
  count = 0
  direction = 0
  passwordLength = len(myPassword)
  for c in clean_string:
    intC = ord(c)
    if intC > 126:
      return "Error"
    if intC < 32:
      return "Error"
    offset = ord(myPassword[count])
    if direction == 0:
      newIntC = intC + offset
    else:
      newIntC = intC - offset
    direction = direction * -1 + 1
    if newIntC > 126:
      newIntC = newIntC - 95
      if newIntC > 126:
        newIntC = newIntC - 95
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

def keyDecrypt(myEncodedString, myPassword):
  newString = ""
  for c in myPassword:
    if ord(c) > 126:
      return "Error"
  count = 0
  direction = 0
  passwordLength = len(myPassword)
  for c in myEncodedString:
    intC = ord(c)
    if intC > 126:
      return "Error"
    if intC < 32:
      return "Error"
    offset = ord(myPassword[count])
    if direction == 0:
      newIntC = intC - offset
    else:
      newIntC = intC + offset
    direction = direction * -1 + 1
    if newIntC < 32:
      newIntC = newIntC + 95
      if newIntC < 32:
        newIntC = newIntC + 95
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

def keyBruteForce(myEncodedString):
  new_strings = []
  keys_array = []
  keys = []
  # Length of key
  key = ""
  for key_length in range(3, 4):
    # An array for each of the possible lengths of keys
    keys_array.append([])
    keys = [""]
    for place in range(0, key_length):
      keys = for_each_place(keys)
    
  for key in keys:
    possible_message = {"key": key, "message": keyDecrypt(myEncodedString, key)}
    new_strings.append(possible_message)
  return new_strings

def for_each_place(beginnings_of_keys):
  old_beginnings = beginnings_of_keys
  beginnings_of_keys = []
  for beginning in old_beginnings:
    for character in range(97, 123):
      beginnings_of_keys.append(beginning + chr(character))
  return beginnings_of_keys



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
  clean_string = line_break_to_space(plaintext_message)
  newString = ""
  count = 0
  messageLength = len(clean_string)
  for c in clean_string:
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
# - - - - - - - - - - - - - - - - 
# Routes
# - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - -

@app.route("/")
def hello():
  return render_template('index.html')

# - - - - - - - - - - - - - - - -
# Offset:
# - - - - - - - - - - - - - - - -

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Offset
# Encrypt:
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

@app.route("/offset/encrypt", methods=["GET"], strict_slashes=False)
def offset_encrypt_get():
  explanation = "Offset encryption converts each character in your message to it's corresponding ASCII code. " 
  return render_template(
    "offset_encrypt_get.html",
    explanation = explanation
  )

@app.route("/offset/encrypt", methods=["POST"], strict_slashes=False)
def offset_encrypt_post():
  message = request.form.get("message")
  offset = request.form.get("offset")
  if message and offset:
    encrypted_message = offset_encrypt(message, offset)
    message = offset_decrypt(encrypted_message, offset)
    return render_template(
      "offset_encrypt_post.html",
      offset = offset,
      message = message,
      encrypted_message = encrypted_message
    )
  else:
    return render_template(
      "error.html",
      error = "" + str(message) + " -- " + str(offset)
    )
  
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Offset
# Decrypt:
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
@app.route("/offset/decrypt", methods=["GET"], strict_slashes=False)
def offset_decrypt_get():
  explanation = "Offset encryption converts each character in your message to it's corresponding ASCII code. " 
  return render_template(
    "offset_decrypt_get.html",
    explanation = explanation
  )

@app.route("/offset/decrypt", methods=["POST"], strict_slashes=False)
def offset_decrypt_post():
  message = request.form.get("message")
  offset = request.form.get("offset")
  if message and offset:
    decrypted_message = offset_decrypt(message, offset)
    return render_template(
      "offset_decrypt_post.html",
      offset = offset,
      message = message,
      decrypted_message = decrypted_message
    )
  else: 
    return render_template(
      "error.html",
      error = ""
    )

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Offset
# Brute Force:
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
 
@app.route("/offset/brute-force", methods=["GET"], strict_slashes=False)
def offset_brute_force_get():
  explanation = "Offset encryption converts each character in your message to it's corresponding ASCII code. " 
  return render_template(
    "offset_brute_force_get.html",
    explanation=explanation
  )  
  
@app.route("/offset/brute-force", methods=["POST"], strict_slashes=False)
def offset_brute_force_decrypt_post():
  message = request.form.get("message")
  if message:
    start_time = time.time()
    possible_decrypted_messages = offset_brute_force(message)
    end_time = time.time()
    decrypt_time = end_time - start_time
    most_likely_indexes = find_spaces(possible_decrypted_messages)
    most_likely_messages = []
    for index in most_likely_indexes:
      most_likely_messages.append(possible_decrypted_messages[index])
    
    return render_template(
      "offset_brute_force_post.html",
      message = message,
      decrypt_time = round(decrypt_time, 5),
      most_likely_offsets = most_likely_indexes,
      most_likely_messages = most_likely_messages,
      possible_decrypted_messages = possible_decrypted_messages
    )
  else:
    return render_template(
      "error.html",
      error = ""
    )

@app.route("/offset", strict_slashes=False)
def offset():  
  explanation = "Offset encryption converts each character in your message to it's corresponding ASCII code. " 
  return render_template(
    "offset.html",
    explanation = explanation
  )

# - - - - - - - - - - - - - - - -
# Shared Key:

@app.route("/shared-key/encrypt", strict_slashes=False)
def shared_key_encrypt():
  message = request.args.get("message")
  key1 = request.args.get("key1")
  key2 = request.args.get("key2")
  key3 = request.args.get("key3")
  key = key1 + key2 + key3
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
  key1 = request.args.get("key1")
  key2 = request.args.get("key2")
  key3 = request.args.get("key3")
  key = key1 + key2 + key3
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

@app.route("/shared-key/brute-force", strict_slashes=False)
def shared_key_brute_force(): 
  message = request.args.get("message")
  start_time = time.time()
  possible_decrypted_messages = keyBruteForce(message);
  end_time = time.time()
  decrypt_time = end_time - start_time
  return render_template(
  "shared-key-brute-force.html",
  possible_decrypted_messages=possible_decrypted_messages,
  possible_decrypted_messages_length = len(possible_decrypted_messages),
  decrypt_time = round(decrypt_time, 5)
  )
  
@app.route("/shared-key", strict_slashes=False)
def shared_key():
  explanation = ""
  return render_template(
    "shared-key.html",
    explanation=explanation
  )


# - - - - - - - - - - - - - - - - 
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
  explanation = ""
  return render_template(
    "public-key.html",
    explanation=explanation
  )

# - - - - - - - - - - - - - - - -
# Public Directory:

@app.route('/<path:path>', strict_slashes=False)
def send_static(path):
  return send_from_directory('public', path)

if __name__ == "__main__":
  app.run()
