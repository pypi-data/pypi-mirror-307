<!--

Questions / À faire (cf. les commentaires dans le corps du texte) :

- les fichiers à modifier sont bien ceux dans le dossier pressoir ?
- vérifier que ce que je dis est juste.
- compléter quand il manque des infos.
- ajouter des personnalisations possibles (cf. Autres)

-->

::: {.introchapitre}
Modifier les paramètres par défaut pour personnaliser le livre créé.
:::


Par défaut, un ensemble de choix, graphiques et éditoriaux, ont été faits et sont appliqués par le Pressoir. Les paramètres peuvent être personnalisés en modifiant les fichiers présents dans le dossier `pressoir`<!--est-ce que c'est bien ça ?-->, comme par exemple&nbsp;: ajouter un logo, changer la police, modifier les couleurs, définir les termes à afficher dans l'index...



## Ajouter un logo

Un emplacement est prévu pour l'ajout d'un logo en haut à gauche du _header_ (ici **+ LE PRESSOIR +**, cf. `pressoir/static/img/pressoir-logo.png`).

Le fichier du logo, au format png, doit être déposé dans `pressoir/static/img`.

<!-- Compléter avec les autres manip à prévoir :
- est-ce bien la procédure à suivre ?
- est-ce qu'il faut spécifier le nom du fichier quelque part ?
-->


## Modifier la police

Pour changer la police, aller dans `pressoir/static/fonts`.

<!-- Compléter avec les autres manip à prévoir :
- est-ce bien la procédure à suivre ?
- est-ce qu'il faut remplacer le nom des polices quelque part ?
-->


## Choisir les couleurs

Les couleurs (_header_ et _footer_, table des matières, contenus additionnels...) peuvent être définies dans le fichier `book.toml`, dans la section `[theme]`.

!contenuadd(./parametrageCouleurs)


## Définir l'index

Un index est un objet éditorial, sur une page dédiée (`textes/index/index-np.md`), qui présente une liste de termes classés par ordre alphabétique et qui renvoie aux endroits où ces termes sont cités tout au long du texte. Un index peut être constitué de plusieurs catégories.

Exemples de catégorie&nbsp;: Personnalités, Lieux, Organismes, Concepts...

L'index utilise le [balisage infra-textuel](chapitre3.html#balisage-infra-textuel).

Au préalable, il est nécessaire de déclarer, dans la section `[indexes]` du fichier `book.toml`, les étiquettes de balise (`ids`) ainsi que le nom des catégories qui leur seront associées (`names`).

L'étiquette de balise (`ids`) ne sera pas visible pour les lecteur.rice.s. Elle ne doit pas comporter d'accent ou d'espace (ex&nbsp;: `personnalite`).

Le nom de chaque catégorie (`names`) sera visible par tou.te.s sur la page «&nbsp;Index&nbsp;» du livre produit (ex&nbsp;: Personnalités).


!contenuadd(./parametrageIndex)


<!--
est-ce qu'on est obligé de rester dans les étiquettes déjà déclarées ou peut-on en créer adhoc ? Si on en crée une adhoc, il faut aussi créer notamment le picto
-->


## Autres (précisez)

- ajouter/modifier un pictogramme (dans `public/static/svg`) - pour balises, contenus additionnels + éléments de navigation ?
- css ?
- est-ce que je rapatrie sur cette page les personnalisation édito de type livre co, parties dans la toc... ?
