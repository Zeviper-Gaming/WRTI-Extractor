"""
update_from_WTRTI.py - Petit script autonome qui met à jour "fm_data_db.csv" dans ce
projet à partir de la version présente côté WTRTI (copie du fichier + conversion du
séparateur ";"/"," attendu par ce programme).

Équivalent à activer UPDATE_WTRTI_DATA=True dans main.py, mais sans enchaîner le reste
du pipeline (génération/écriture des .cfg). À lancer depuis le dossier "src/" (import
relatif "function").
"""
import function as func

func.update_wtrti_data()

print("Data was updated from WTRTI")