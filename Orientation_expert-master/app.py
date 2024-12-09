import json
from fpdf import FPDF
from flask import Flask, render_template, request,  send_file
from io import BytesIO
from reportlab.pdfgen import canvas
app = Flask(__name__)
app.secret_key = 'votre_clé_secrète_pour_flash'  # Remplacez par une clé sécurisée


# Charger la base des règles
def charger_regles():
    with open('rules.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Fonction pour appliquer les règles (sans le niveau d'études)
def consulter_filiere(moyenne, matieres, secteur):
    regles = charger_regles()
    resultats = []
    
    for filiere in regles:
        conditions = filiere['conditions']
        
        # Vérifier les conditions de moyenne, de matières et de secteur
        if (moyenne >= conditions['moyenne_min'] and
            any(matiere in matieres for matiere in conditions['matieres']) and
            (secteur == 'Tout' or secteur in filiere['secteur'])):
            resultats.append(filiere)
            
    return resultats
@app.route('/orientation')
def orientation():
    return render_template('orientation.html')

# Route pour afficher le formulaire
@app.route('/')
def index():
    return render_template('index.html')

# Route pour traiter le formulaire et afficher les résultats
@app.route('/obtenir_resultats', methods=['POST'])
def obtenir_resultats():
    # Récupérer les données du formulaire
    moyenne = float(request.form['moyenne'])
    matieres = request.form.getlist('matieres')
    secteur = request.form['secteur']
    
    # Appliquer les règles pour obtenir les résultats
    resultats = consulter_filiere(moyenne, matieres, secteur)
    
    return render_template('resultats.html', resultats=resultats)
@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Get user selections from the form
    selections = [request.form.get(f'choix{i}') for i in range(1, 7)]
    
    # Define a mapping of option values to human-readable descriptions
    options_map = {
    # Informatique
    "Option1_1": "Informatique : Faculté des Sciences de Tunis (FST)",
    "Option1_2": "Informatique : Sup'Com",
    "Option1_3": "Informatique : Institut Supérieur d'Informatique de Mahdia",
    "Option1_4": "Informatique : Faculté des Sciences de Sfax",

    # Médecine
    "Option2_1": "Médecine : Faculté de Médecine de Tunis",
    "Option2_2": "Médecine : Faculté de Médecine de Monastir",
    "Option2_3": "Médecine : Faculté de Médecine de Sfax",

    # Sciences économiques
    "Option3_1": "Sciences économiques : FSEG Tunis",
    "Option3_2": "Sciences économiques : IHEC Sousse",
    "Option3_3": "Sciences économiques : IHEC Carthage",
    "Option3_4": "Sciences économiques : FSEG Sfax",

    # Architecture
    "Option4_1": "Architecture : École Nationale d'Architecture et d'Urbanisme (ENAU)",

    # Génie civil
    "Option5_1": "Génie civil : École Nationale d'Ingénieurs de Tunis (ENIT)",
    "Option5_2": "Génie civil : École Nationale d'Ingénieurs de Sfax (ENIS)",
    "Option5_3": "Génie civil : École Nationale d'Ingénieurs de Monastir (ENIM)",

    # Pharmacie
    "Option6_1": "Pharmacie : Faculté de Pharmacie de Monastir",

    # Littérature
    "Option7_1": "Littérature : Faculté des Lettres, des Arts et des Humanités de la Manouba",
    "Option7_2": "Littérature : Faculté des Lettres et Sciences Humaines de Sousse",

    # Droit
    "Option8_1": "Droit : Faculté des Sciences Juridiques de Tunis",
    "Option8_2": "Droit : Faculté des Sciences Juridiques de Sfax",

    # Ingénierie électrique
    "Option9_1": "Ingénierie électrique : École Nationale d'Ingénieurs de Tunis (ENIT)",
    "Option9_2": "Ingénierie électrique : École Supérieure des Communications de Tunis (Sup'Com)",

    # Sciences agronomiques
    "Option10_1": "Sciences agronomiques : Institut National Agronomique de Tunisie (INAT)",
    "Option10_2": "Sciences agronomiques : École Supérieure d'Agriculture de Mograne",

    # Design graphique
    "Option11_1": "Design graphique : École Supérieure des Sciences et Technologies du Design (ESSTD)"
}

    
    # Create the PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)  # Set font to Arial, bold, size 16
    pdf.cell(200, 10, txt="Options Sélectionnées", ln=True, align='C')

    pdf.ln(10)
 
    pdf.set_font("Arial", '', 12)
    for i, selection in enumerate(selections, start=1):
        description = options_map.get(selection, "Option inconnue")
        pdf.cell(20, 10, str(i), border=1, align='C')  # Option number column
        pdf.cell(170, 10, description, border=1, align='L')  # Option description column
        pdf.ln()  # Line break for the next row


    # Save the PDF to a file
    pdf_file_path = "selections.pdf"
    pdf.output(pdf_file_path)

    # Send the PDF file to the user
    return send_file(pdf_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
