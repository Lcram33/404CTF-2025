# Earth Attack (0/2)

## Énoncé

> Les malfrats qui ont été arrétés sont déjà connus de nos services... Ils étaient soupçonnés d'avoir saboté un moteur d'avion en guise d'entraînement. Il s'agissait d'un petit Cessna en France, les dégâts étaient importants et le pilote avait été légèrement blessé donc le BEA avait enquêté dessus à l'époque...
> 
> Quelle était l'immatriculation de l'avion en question ?
> 
> Format du flag : 404CTF{1Z-ABC}

<h2>Solution</h2>

<details>
<summary></summary>

### Analyse de l'énoncé

> Les malfrats qui ont été **arrétés** sont déjà connus de nos services...
> 
> Ils étaient soupçonnés d'avoir **saboté** un **moteur** d'avion en guise d'entraînement.
> 
> Il s'agissait d'un petit **Cessna** en **France**, les dégâts étaient importants et le **pilote** avait été légèrement **blessé** donc le **BEA** avait enquêté dessus à l'époque...

### Flag

* Un simple google dork :
  * `"Cessna" "blessé" "bea"`
* Il s'agit du 4e résultat (PDF)
  * https://bea.aero/fileadmin/user_upload/9H-MDJ.pdf

`404CTF{9H-MDJ}`

*Le [document](9H-MDJ.pdf) est joint dans ce dossier.*

</details>