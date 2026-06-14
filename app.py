import os
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
from brevo import Configuration, ApiClient
from brevo.api import transactional_emails_api
from brevo.model.send_smtp_email import SendSmtpEmail
from brevo.model.send_smtp_email_to import SendSmtpEmailTo

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-key-change-in-production")

def envoyer_email(nom, email_visiteur, sujet, message):
    """Envoie un email via l'API Brevo"""
    # Configuration de l'API
    configuration = Configuration()
    configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")
    api_client = ApiClient(configuration)
    api_instance = transactional_emails_api.TransactionalEmailsApi(api_client)

    # Destinataire (l'ONG)
    destinataire = SendSmtpEmailTo(
        email=os.getenv("EMAIL_DESTINATAIRE"),
        name="SLIFE WORLD"
    )

    # Construction de l'email
    email_brevo = SendSmtpEmail(
        to=[destinataire],
        sender={
            "name": "SLIFE WORLD",
            "email": os.getenv("EMAIL_EXPEDITEUR")
        },
        subject=f"[SLIFE WORLD] {sujet}",
        html_content=f"""<html>
            <body>
                <h3>Nouveau message depuis le site SLIFE WORLD</h3>
                <p><strong>Nom :</strong> {nom}</p>
                <p><strong>Email :</strong> {email_visiteur}</p>
                <p><strong>Sujet :</strong> {sujet}</p>
                <p><strong>Message :</strong></p>
                <p>{message.replace(chr(10), '<br>')}</p>
            </body>
        </html>""",
        text_content=f"Nom : {nom}\nEmail : {email_visiteur}\nSujet : {sujet}\n\nMessage :\n{message}"
    )

    # Envoi
    response = api_instance.send_transac_email(email_brevo)
    print(f"Email envoyé via Brevo, message ID : {response.message_id}")

# Routes (inchangées)
@app.route("/")
def accueil():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    nom = request.form.get("user_name", "").strip()
    email = request.form.get("user_email", "").strip()
    sujet = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()
    
    if not all([nom, email, sujet, message]):
        flash("Tous les champs sont obligatoires.", "danger")
        return redirect(url_for("accueil") + "#contact")
    
    if "@" not in email or "." not in email:
        flash("Veuillez entrer une adresse email valide.", "danger")
        return redirect(url_for("accueil") + "#contact")
    
    try:
        envoyer_email(nom, email, sujet, message)
        flash("Votre message a été envoyé avec succès. Nous vous répondrons sous 48h.", "success")
    except Exception as e:
        print(f"Erreur Brevo : {e}")
        flash(f"Erreur technique : {str(e)}. Veuillez réessayer ou nous appeler.", "danger")
    
    return redirect(url_for("accueil") + "#contact")

@app.route("/environnement.html")
def environnement():
    return render_template("environnement.html")

@app.route("/population.html")
def population():
    return render_template("population.html")

@app.route("/gestion.html")
def gestion():
    return render_template("gestion.html")

@app.route("/publications")
def publications():
    return render_template("publications.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)