import os
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-key-change-in-production")

def envoyer_email(nom, email_visiteur, sujet, message):
    """Envoie un email via SendGrid (API, pas SMTP)"""
    message_email = Mail(
        from_email=os.getenv("EMAIL_EXPEDITEUR"),
        to_emails=os.getenv("EMAIL_DESTINATAIRE"),
        subject=f"[SLIFE WORLD] {sujet}",
        plain_text_content=f"Nom : {nom}\nEmail : {email_visiteur}\n\nMessage :\n{message}"
    )
    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    reponse = sg.send(message_email)
    print(f"SendGrid response statut: {reponse.statuts_code}")

# Le reste de ton code (routes, etc.) reste identique
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
        flash(f"Erreur technique : {str(e)}. Veuillez réessayer ou nous appeler.", "danger")
    
    return redirect(url_for("accueil") + "#contact")

# Routes pour les autres pages
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
