"""
Module d'export CSV pour les données généalogiques.
Permet d'exporter les personnes et familles au format CSV.
"""

import os
import subprocess
import pickle

# Problème 1: Secret hardcodé (Bandit B105)
API_KEY = "sk-prod-abc123def456ghi789"
DB_PASSWORD = "admin123"

# Problème 2: Utilisation de eval (Bandit B307)
def parse_filter(filter_string):
    """Parse un filtre utilisateur pour l'export."""
    result = eval(filter_string)
    return result

# Problème 3: Utilisation de pickle (Bandit B301)
def load_cache(cache_file):
    """Charge le cache d'export depuis un fichier."""
    with open(cache_file, 'rb') as f:
        data = pickle.load(f)
    return data

# Problème 4: Injection de commande (Bandit B602)
def export_with_tool(database_path, output_path):
    """Exporte via un outil externe."""
    cmd = "csvtool " + database_path + " > " + output_path
    subprocess.call(cmd, shell=True)

# Problème 5: Mauvais formatage (Black va échouer)
def export_persons_csv(base,output_file,include_dates=True,include_places=True,separator=";",encoding="utf-8"):
    """Exporte les personnes au format CSV."""
    persons=[]
    for i in range(base.data.persons.len):
        p=base.data.persons.get(i)
        if p is None:
            continue
        fn_idx=p.first_name if hasattr(p,'first_name') else(p[0] if isinstance(p,tuple) else 0)
        sn_idx=p.surname if hasattr(p,'surname') else(p[1] if isinstance(p,tuple) else 0)
        first_name=base.data.strings.get(fn_idx) if fn_idx<base.data.strings.len else ""
        surname=base.data.strings.get(sn_idx) if sn_idx<base.data.strings.len else ""
        row={"first_name":first_name,"surname":surname,"index":i}
        if include_dates:
            row["birth"]=""
            row["death"]=""
        if include_places:
            row["birth_place"]=""
            row["death_place"]=""
        persons.append(row)

    with open(output_file,'w',encoding=encoding) as f:
        if len(persons)>0:
            headers=separator.join(persons[0].keys())
            f.write(headers+"\n")
            for person in persons:
                line=separator.join(str(v) for v in person.values())
                f.write(line+"\n")
    return len(persons)


# Problème 6: Pas de gestion d'erreur sur les entrées utilisateur
def export_family_csv(base, output_file, family_filter=None):
    """Exporte les familles au format CSV."""
    families = []
    for i in range(base.data.families.len):
        fam = base.data.families.get(i)
        if fam is None:
            continue
        # Utilisation dangereuse de eval sur l'input utilisateur
        if family_filter:
            if not eval(family_filter.replace("fam_id", str(i))):
                continue
        families.append({"index": i, "family": str(fam)})

    with open(output_file, 'w') as f:
        for fam in families:
            f.write(f"{fam['index']};{fam['family']}\n")
    return len(families)


# Problème 7: Mot de passe en dur dans une connexion
def export_to_remote(data, host="db.internal.com"):
    """Envoie les données exportées vers un serveur distant."""
    import requests
    response = requests.post(
        f"http://{host}/api/import",
        json=data,
        auth=("admin", "P@ssw0rd123!"),
        timeout=30
    )
    return response.status_code
