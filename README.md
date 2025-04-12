# IPM_FSPI_CTAR_Rage

La rage est une maladie zoonotique, dont l'endémicité à Madagascar est documentée depuis environ 50 ans. Les estimations officielles parlent de 800 victimes de cette maladie chaque année, mais elles sont probablement sous-estimées.

Afin de contrôler cette maladie, le Ministère de Santé avec le soutien de l’Institut Pasteur de Madagascar (IPM) a mis en place 31 Centres de Traitements Anti-Rabbiques (CTAR), dont une à la capitale du pays et le reste dans les régions. Chaque année, environ 15,000 patients reçoivent le traitement post-exposition au sein d’un de ces CTARs. Chaque personne ayant subi une exposition à la rage (morsure ou autres interactions avec un animal) et cherchant les services d’un CTAR est évaluée et enregistrée dans une base des données.

Au sein des CTARs périphériques, ces consultations sont enregistrées dans un formulaire en papier remplie, qui est ensuite envoyé au CTAR de IPM et saisie dans une base des données de système RedCap. Les patients évalués au niveau de CTAR de IPM sont enregistrés directement dans une base des données basée sur MS Access.

Les données sont extraites et analysées annuellement pour tirer les indicateurs de performance des CTAR et autres indicateurs épidémiologiques, importants pour améliorer la gestion de la maladie à l’échelle nationale.

Les deux bases des données (données originaires de CTAR périphériques et données originaires de CTAR de IPM) ne sont pas harmonisées; les variables sont codées différemment, les questionnaires ne sont pas exactement les mêmes, bien qu’ils ciblent les mêmes indicateurs. Certaines variables ne sont pas standardisées au niveau d'orthographe. En plus de cela, une troisième base de données réunit les commandes du vaccin effectuées par chaque CTAR périphérique au niveau de CTAR de IPM.

Jusqu’à présent, un rapport annuel est élaboré chaque année pour résumer les indicateurs principaux des bases de données rage. Plusieurs scripts en R existent pour analyser les deux bases des données (CTAR périphérique et CTAR de IPM), mais ces derniers sont difficilement reproductibles sur les données annuelles.
