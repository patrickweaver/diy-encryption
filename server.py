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
    if ord(string_list[i]) == 13:
      string_list[i] = " "
    if ord(string_list[i]) == 10:
      string_list[i] = ""
  return "".join(string_list)

# - - - - - - - - - - - - - - - -
# To find the decrypted strings with the most spaces
# - - - - - - - - - - - - - - - -

def find_spaces(my_possible_strings, include_e_a, how_many):
  spaces_list = []
  for i in range(0, len(my_possible_strings)):
    spaces = 0
    for c in my_possible_strings[i]:
      if ord(c) == 32:
        spaces += 1
      if (include_e_a):
        if ord(c) == 101 or ord(c) == 97:
          spaces += 1
    spaces_list.append({"spaces": spaces, "index": i})
                 
  spaces_list = sorted(spaces_list, key=lambda k: k["spaces"], reverse=True)


  most_likely_indexes = []
  for i in range(0, how_many):
    most_likely_indexes.append(spaces_list[i]["index"])
                 
  return most_likely_indexes


# - - - - - - - - - - - - - - - - 
# To use just the messages
# - - - - - - - - - - - - - - - - 

def isolate_messages(n):
      return n['message']


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

def shared_key_encrypt(my_string, my_key):
  clean_string = line_break_to_space(my_string)
  new_string = ""
  for c in my_key:
    if ord(c) > 126:
      return "Error"
  count = 0
  #direction = 0
  key_length = len(my_key)
  for c in clean_string:
    int_c = ord(c)
    if int_c > 126:
      return "Error"
    if int_c < 32:
      return "Error"
    offset = ord(my_key[count])
    #if direction == 0:
    #  new_int_c = int_c + offset
    #else:
    #  new_int_c = int_c - offset
    new_int_c = int_c + offset
    #direction = direction * -1 + 1
    if new_int_c > 126:
      new_int_c = new_int_c - 95
      if new_int_c > 126:
        new_int_c = new_int_c - 95
    #if new_int_c < 32:
    #  new_int_c = new_int_c + 95
    #  if new_int_c < 32:
    #    new_int_c = new_int_c + 95
    new_char = chr(new_int_c)
    new_string += new_char
    
    count += 1
    if count == key_length:
      count = 0
  return new_string

def shared_key_decrypt(my_encoded_string, my_key):
  new_string = ""
  for c in my_key:
    if ord(c) > 126:
      return "Error"
  count = 0
  #direction = 0
  key_length = len(my_key)
  for c in my_encoded_string:
    int_c = ord(c)
    if int_c > 126:
      return "Error"
    if int_c < 32:
      return "Error"
    offset = ord(my_key[count])
    #if direction == 0:
    #  new_int_c = int_c - offset
    #else:
    #  new_int_c = int_c + offset
    new_int_c = int_c - offset
    #direction = direction * -1 + 1
    if new_int_c < 32:
      new_int_c = new_int_c + 95
      if new_int_c < 32:
        new_int_c = new_int_c + 95
    #if new_int_c > 126:
    #  new_int_c = new_int_c - 95
    #  if new_int_c > 126:
    #    new_int_c = new_int_c - 95
    new_char = chr(new_int_c)
    new_string += new_char
    
    count += 1
    if count == key_length:
      count = 0
  return new_string

def shared_key_brute_force(my_encoded_string):
  new_strings = []
  keys_array = []
  keys = []
  key = ""
  # Currently this only looks at 3 letter keys but this range could be expanded
  for key_length in range(3, 4):
    # An array for each of the possible lengths of keys
    keys_array.append([])
    keys = [""]
    for place in range(0, key_length):
      keys = for_each_place(keys)
    
  for key in keys:
    possible_message = {"key": key, "message": shared_key_decrypt(my_encoded_string, key)}
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
primes = [11, 13, 17, 19, 23, 29]

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def coprime(a, b):
    return gcd(a, b) == 1
  
def get_coprimes(prime_1, prime_2):
  larger_prime = prime_1
  if (prime_1 - prime_2) < 0:
    larger_prime = prime_2
  modulus = prime_1 * prime_2
  coprimes_of = (prime_1 - 1) * (prime_2 - 1)
  coprimes = []
  for n in range(larger_prime + 2, coprimes_of):
    if coprime(n, coprimes_of):
      if generate_keys(prime_1, prime_2, n):
        coprimes.append(n)
  return coprimes
  
def generate_keys(prime_1, prime_2, coprime):
  modulus = prime_1 * prime_2
  coprimes_of = (prime_1 - 1) * (prime_2 - 1)
  encrypt_exponent = coprime
  decrypt_exponent = 0
  public_keys = [encrypt_exponent, modulus]
  for n in range(2, coprimes_of):
    # Find largest decrypt_exponent:
    if (n * encrypt_exponent) % coprimes_of == 1:
      decrypt_exponent = n
  if decrypt_exponent  == 0:
    return False
  private_keys = [decrypt_exponent, modulus]
  if public_keys == private_keys:
    return False
  return {
    "public_keys": public_keys,
    "private_keys": private_keys
  }
  

def public_key_encrypt(plaintext_message, public_keys):
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
  
def public_key_decrypt(encrypted_message, private_keys):
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
    decrypted_int = (i ** private_keys[0] % private_keys[1])
    if decrypted_int > 126:
      decrypted_string = "Error: Invalid message"
      break;
    decrypted_string += chr(decrypted_int)
  return decrypted_string

def public_key_brute_force(my_encoded_string):
  new_strings = []
  keys = []
  largest_prime = primes[len(primes) - 1]
  # Prime 1
  for prime_1 in primes:
    for prime_2 in primes:
      if prime_1 != prime_2:
        coprimes = get_coprimes(prime_1, prime_2)
        for coprime in coprimes:
          keys.append(generate_keys(prime_1, prime_2, coprime)["private_keys"])
          
  unique_keys = [];
  unique_key_strings = [];
  
  for key in keys:
    key_string = str(key[0]) + '-' + str(key[1])
    try:
      key_string_index = unique_key_strings.index(key_string)
    except ValueError:
      key_string_index = -1
    
    if (key_string_index == -1):
      unique_keys.append(key)
      unique_key_strings.append(key_string)
          
  for key in unique_keys:
    possible_message = {"key": key, "message": public_key_decrypt(my_encoded_string, key)}
    new_strings.append(possible_message)
  return new_strings



# - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - 
# Routes
# - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - -

@app.route("/")
def hello():
  return render_template('index.html')

# - - - - - - - - - - - - - - - -
# * * * * * *
# * Offset  *
# * * * * * *
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
    explanation = explanation,
    encrypt = "active"
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
      encrypted_message = encrypted_message,
      encrypt = "active"
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
    explanation = explanation,
    decrypt = "active"
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
      decrypted_message = decrypted_message,
      decrypt = "active"
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
    explanation=explanation,
    brute_force = "active"
  )  
  
@app.route("/offset/brute-force", methods=["POST"], strict_slashes=False)
def offset_brute_force_decrypt_post():
  message = request.form.get("message")
  if message:
    start_time = time.time()
    possible_decrypted_messages = offset_brute_force(message)
    end_time = time.time()
    decrypt_time = end_time - start_time
    most_likely_indexes = find_spaces(possible_decrypted_messages, False, 3)
    most_likely_messages = []
    for index in most_likely_indexes:
      most_likely_messages.append(possible_decrypted_messages[index])
    
    return render_template(
      "offset_brute_force_post.html",
      message = message,
      decrypt_time = round(decrypt_time, 5),
      most_likely_offsets = most_likely_indexes,
      most_likely_messages = most_likely_messages,
      possible_decrypted_messages = possible_decrypted_messages,
      brute_force = "active"
    )
  else:
    return render_template(
      "error.html",
      error = ""
    )
  
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Offset
# Index:
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

@app.route("/offset", strict_slashes=False)
def offset():  
  explanation = "Offset encryption converts each character in your message to it's corresponding ASCII code. " 
  return render_template(
    "offset.html",
    explanation = explanation
  )

# - - - - - - - - - - - - - - - -
# * * * * * * * *
# * Shared Key  *
# * * * * * * * *
# - - - - - - - - - - - - - - - -

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Shared Key
# Encrypt:
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

@app.route("/shared-key/encrypt", methods=["GET"], strict_slashes=False)
def shared_key_encrypt_get():
  explanation = ""
  return render_template(
    "shared_key_encrypt_get.html",
    explanation = explanation,
    encrypt = "active"
  )

@app.route("/shared-key/encrypt", methods=["POST"], strict_slashes=False)
def shared_key_encrypt_post():
  message = request.form.get("message")
  key_1 = request.form.get("key1").lower()
  key_2 = request.form.get("key2").lower()
  key_3 = request.form.get("key3").lower()
  key = key_1 + key_2 + key_3
  if message and key:
    encrypted_message = shared_key_encrypt(message, key)
    return render_template(
    "shared_key_encrypt_post.html",
    key = key,
    message = message,
    encrypted_message = encrypted_message,
    encrypt = "active"
    )
  else:
    return render_template("error.html")

  
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Shared Key
# Decrypt:
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

@app.route("/shared-key/decrypt", methods=["GET"], strict_slashes=False)
def shared_key_decrypt_get():
  explanation = ""
  return render_template(
    "shared_key_decrypt_get.html",
    explanation = explanation,
    decrypt = "active"
  )  
  
@app.route("/shared-key/decrypt", methods=["POST"], strict_slashes=False)
def shared_key_decrypt_post():
  message = request.form.get("message")
  key_1 = request.form.get("key1").lower()
  key_2 = request.form.get("key2").lower()
  key_3 = request.form.get("key3").lower()
  key = key_1 + key_2 + key_3
  if message and key:
    decrypted_message = shared_key_decrypt(message, key)
    return render_template(
    "shared_key_decrypt_post.html",
    key = key,
    message = message,
    decrypted_message = decrypted_message,
    decrypt = "active"
    )
  else:
    return render_template("error.html")

  
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Shared Key
# Brute Force:
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

@app.route("/shared-key/brute-force", methods=["GET"], strict_slashes=False)
def shared_key_brute_force_get():
  explanation = ""
  return render_template(
    "shared_key_brute_force_get.html",
    explanation = explanation,
    brute_force = "active"
  )  
  
@app.route("/shared-key/brute-force", methods=["POST"], strict_slashes=False)
def shared_key_brute_force_post(): 
  message = request.form.get("message")
  if message:
    start_time = time.time()
    possible_decrypted_messages = shared_key_brute_force(message);
    end_time = time.time()
    decrypt_time = end_time - start_time
    
    messages_only = list(map(isolate_messages, possible_decrypted_messages))
    most_likely_indexes = find_spaces(messages_only, True, 5)
    most_likely_messages = []
    for index in most_likely_indexes:
      most_likely_messages.append(possible_decrypted_messages[index])
      
    return render_template(
      "shared_key_brute_force_post.html",
      message = message,
      possible_decrypted_messages = possible_decrypted_messages,
      possible_decrypted_messages_length = len(possible_decrypted_messages),
      most_likely_offsets = most_likely_indexes,
      most_likely_messages = most_likely_messages,
      most_likely_messages_length = len(most_likely_indexes),
      decrypt_time = round(decrypt_time, 5),
      brute_force = "active"
    )
  else:
    return render_template(
      "error.html"
    )


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Shared Key
# Index:
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 
  
@app.route("/shared-key", strict_slashes=False)
def shared_key():
  explanation = ""
  return render_template(
    "shared-key.html",
    explanation = explanation
  )


# - - - - - - - - - - - - - - - -
# * * * * * * * *
# * Public Key  *
# * * * * * * * *
# - - - - - - - - - - - - - - - -

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Public Key
# Generate Keys:
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

@app.route("/public-key/generate-keys", methods=["GET"], strict_slashes=False)
def public_key_generate_keys_get():
  explanation = ""
  return render_template(
    "public_key_generate_keys_get.html",
    explanation = explanation,
    primes = primes,
    generate_keys = "active"
  )

@app.route("/public-key/primes", methods=["POST"], strict_slashes=False)
def available_coprimes():
  prime_1 = int(request.form.get("prime1"))
  prime_2 = int(request.form.get("prime2"))
  larger_prime = prime_1
  if (prime_1 - prime_2) < 0:
    larger_prime = prime_2
  modulus = prime_1 * prime_2
  coprimes_of = (prime_1 - 1) * (prime_2 - 1)
  coprimes = []
  for n in range(larger_prime + 2, coprimes_of):
    if coprime(n, coprimes_of):
      if generate_keys(prime_1, prime_2, n):
        coprimes.append(n)
  return jsonify(coprimes)

@app.route("/public-key/keys", methods=["POST"], strict_slashes=False)
def keys():
  prime_1 = int(request.form.get("prime1"))
  prime_2 = int(request.form.get("prime2"))
  coprime = int(request.form.get("coprime"))
  keys = generate_keys(prime_1, prime_2, coprime)
  if keys:
    return jsonify({"publicKeys": keys["public_keys"], "privateKeys": keys["private_keys"]})
  else:
    return jsonify({"error": "No keys found, select different numbers (probably higher numbers)."})  
  
  
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Public Key
# Encrypt:
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

@app.route("/public-key/encrypt", methods=["GET"], strict_slashes=False)
def public_key_encrypt_get():
  explanation = ""
  return render_template(
    "public_key_encrypt_get.html",
    explanation = explanation,
    encrypt = "active"
  )

@app.route("/public-key/encrypt", methods=["POST"], strict_slashes=False)
def public_key_encrypt_post():
  public_key = []
  public_key.append(int(request.form.get("public-key-1")))
  public_key.append(int(request.form.get("public-key-2")))
  message = request.form.get("message")
  if public_key and message:
    return render_template(
      "public_key_encrypt_post.html",
      public_keys = public_key,
      message = message,
      encrypted_message = public_key_encrypt(message, public_key),
      encrypt = "active"
    )
  else:
    return render_template("error.html")

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Public Key
# Decrypt:
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

@app.route("/public-key/decrypt", methods=["GET"], strict_slashes=False)
def public_key_decrypt_get():
  explanation = ""
  return render_template(
    "public_key_decrypt_get.html",
    explanation = explanation,
    decrypt = "active"
  )

@app.route("/public-key/decrypt", methods=["POST"], strict_slashes=False)
def public_key_decrypt_post():
  private_keys = []
  private_keys.append(int(request.form.get("private-key-1")))
  private_keys.append(int(request.form.get("private-key-2")))
  message = request.form.get("message")
  if private_keys and message:
    return render_template(
      "public_key_decrypt_post.html",
      private_keys = private_keys,
      encrypted_message = message,
      decrypted_message = public_key_decrypt(message, private_keys),
      decrypt = "active"
    )
  else:
    return render_template(
      "error.html"
    )

  # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Public Key
# Brute Force:
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

@app.route("/public-key/brute-force", methods=["GET"], strict_slashes=False)
def public_key_brute_force_get():
  explanation = ""
  return render_template(
    "public_key_brute_force_get.html",
    explanation = explanation,
    brute_force = "active"
  )  
  
@app.route("/public-key/brute-force", methods=["POST"], strict_slashes=False)
def public_key_brute_force_post(): 
  message = request.form.get("message")
  if message:
    start_time = time.time()
    possible_decrypted_messages = public_key_brute_force(message);
    end_time = time.time()
    decrypt_time = end_time - start_time

    # Isolate messages
    messages_only = list(map(isolate_messages, possible_decrypted_messages))
    
    # Identify valid messages
    for index, decrypted_message in enumerate(messages_only, start=0):
      if decrypted_message == "Error: Invalid message":
        possible_decrypted_messages[index]['valid'] = False
      else:
        possible_decrypted_messages[index]['valid'] = True
        
    return render_template(
      "public_key_brute_force_post.html",
      message = message,
      possible_decrypted_messages = possible_decrypted_messages,
      possible_decrypted_messages_length = len(possible_decrypted_messages),
      decrypt_time = round(decrypt_time, 5),
      brute_force = "active"
    )
  else:
    return render_template(
      "error.html"
    )
  
  
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Public Key
# Index:
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

@app.route("/public-key", strict_slashes=False)
def public_key():
  explanation = ""
  return render_template(
    "public-key.html",
    explanation = explanation
  )

# - - - - - - - - - - - - - - - -
# * * * * * * * * * * *
# * Public Directory  *
# * * * * * * * * * * *
# - - - - - - - - - - - - - - - -

@app.route('/<path:path>', strict_slashes=False)
def send_static(path):
  return send_from_directory('public', path)

if __name__ == "__main__":
  app.run()
