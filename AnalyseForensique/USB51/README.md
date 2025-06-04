# USB 51

![challenge](challenge.png)

## Fichier du challenge

* **capture.pcapng** : dump wireshark du challenge (non modifié)

<h2>Solution</h2>

<details>
<summary></summary>

L'astuce ici est de trier les paquets par taille. Un paquet sort du lot (beaucoup plus gros que les autres).

![step1](solve/step1.png)

On l'ouvre, et on lit du contenu qui suggère qu'un fichier PDF a été transmis.

![step2](solve/step2.png)

On enregistre les données dans un fichier.

![step3](solve/step3.png)

Dans le PDF obtenu (qui semble contenir des informations sur un projet "critique"), une chaîne binaire est fournie. Après conversion, il s'agit du flag.

</details>
