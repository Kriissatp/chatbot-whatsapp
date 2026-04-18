from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

sesiones = {}

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == "mitoken123":
        return challenge
    return "Token inválido", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    numero = request.values.get("From", "")
    
    resp = MessagingResponse()
    msg = resp.message()
    
    paso = sesiones.get(numero, 0)
    
    if paso == 0:
        msg.body("Para ayudarte necesito me indiques tu Nombre y Rut?")
        sesiones[numero] = 1
    elif paso == 1:
        msg.body("Gracias, ahora indícame tu dirección y el plan que necesitas contratar, para hacer una evaluacion previa y ver que promociones tenemos disponibles.")
        sesiones[numero] = 2
    elif paso == 2:
        msg.body("¡Perfecto! Hemos recibido tus datos. En breve te daremos la información sobre los planes.")
        sesiones[numero] = 3
    elif paso == 3:
        return str(resp)
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
