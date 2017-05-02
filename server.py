import sys

from flask import Flask, send_from_directory, jsonify, request, render_template
app = Flask(__name__, static_folder='views')

data = {
  "dreams": [
    "2",
    5,
    "Hello!"
  ],
  "messages": []
}



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

@app.route("/")
def hello():
  return app.send_static_file('index.html')

@app.route("/dreams", methods=["GET"])
def get_dreams():
  return jsonify(**data)

@app.route("/dreams", methods=["POST"])
def add_dream():
  data["dreams"].append(request.args["dream"])
  return '"OK"'

@app.route("/messages", methods=["GET"])
def get_messages():
  return jsonify(**data)

@app.route("/offset/encrypt")
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
    return app.send_static_file("offset-.html")

@app.route("/offset")
def offset():
  return app.send_static_file("offset.html")

@app.route('/<path:path>')
def send_static(path):
  return send_from_directory('public', path)

if __name__ == "__main__":
  app.run()
