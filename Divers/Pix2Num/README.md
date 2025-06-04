# Pix2Num

![challenge](challenge.png)

## Fichiers du challenge

* **encrypt.py** : fichier original du challenge (non modifié)
* **number.txt** : fichier original du challenge (non modifié)
* **solve.py** : résolution du challenge

<h2>Solution</h2>

<details>
<summary></summary>

Ce programme transforme les pixels d'une image en nombres qu'il "chiffre".
Il utilise pour cela une clé, qu'il XOR avec les nombres obtenus.

Mais... La clé est générée aléatoirement et n'est pas stockée dans le fichier `encrypt.py` !

Comment faire alors ? On exploite la propriété du XOR : $\forall a \in [0, 1], a \oplus 0 = a$
et on retrouve ainsi la clé, qui est vers le bas du fichier (pixels blancs).

</details>
