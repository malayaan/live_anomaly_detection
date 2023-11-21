import os
import time
import shutil

# Chemins des dossiers source et destination
dossier_source = 'data2'
dossier_destination = 'data1'

while True:
    # Liste tous les fichiers dans le dossier source
    fichiers = [f for f in os.listdir(dossier_source) if f.endswith('.json')]

    for fichier in fichiers:
        # Chemin complet du fichier source et destination
        source = os.path.join(dossier_source, fichier)
        destination = os.path.join(dossier_destination, fichier)

        # Déplace le fichier
        shutil.move(source, destination)
        print(f"Fichier {fichier} déplacé de {dossier_source} à {dossier_destination}")

        time.sleep(5)  # Temps en secondes