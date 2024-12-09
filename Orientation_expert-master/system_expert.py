import json

def consulter_filiere(moyenne, matieres, secteur=None, region=None):
    try:
        # Charger les règles depuis le fichier JSON
        with open("rules.json", "r", encoding="utf-8") as f:
            regles = json.load(f)
    except FileNotFoundError:
        print("Le fichier des règles est introuvable.")
        return []
    except json.JSONDecodeError:
        print("Erreur dans le format du fichier JSON.")
        return []
    
    resultats = []
    for filiere in regles:
        conditions = filiere.get('conditions', {})
        
        # Vérification de la moyenne
        moyenne_min = conditions.get('moyenne_min', 0)
        if moyenne < moyenne_min:
            continue
        
        # Vérification des matières
        matieres_requises = conditions.get('matieres', [])
        if not any(matiere in matieres for matiere in matieres_requises):
            continue
        
        # Filtrage par secteur
        if secteur and secteur not in filiere.get('secteur', []):
            continue
        
        # Filtrage par région
        if region:
            universites = filiere.get('universite', [])
            if not any(universite['region'] == region for universite in universites):
                continue
        
        resultats.append(filiere)
    
    return resultats
