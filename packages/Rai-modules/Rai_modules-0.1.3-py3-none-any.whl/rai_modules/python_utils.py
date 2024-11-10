class Chatbot:
    def __init__(self):
        self.questions = {
            'bonjour': 'Bonjour comment allez-vous?',
            'je vais bien': 'Je suis content pour vous',
            'corrige mon code:': 'D\'accord je vais essayer',
            'for keyword, response in': 'Il faut faire for keyword, response in ton_dictionnaire.items()',
            'comment ça va': 'Ça va bien, merci!',
            'quel est ton nom': 'Je suis un chatbot, je n\'ai pas de nom propre.',
            'quel âge as-tu': 'Je n\'ai pas d\'âge, je suis une intelligence artificielle!',
            'que fais-tu': 'Je suis là pour t\'aider avec du code et répondre à tes questions.',
            'quel est ton but': 'Mon but est de t\'aider à apprendre et résoudre des problèmes!',
            'comment t\'appelles-tu': 'Je n\'ai pas de nom, mais tu peux m\'appeler comme tu veux.',
            'quel est ton langage de programmation préféré': 'Je préfère Python, mais je peux aussi t\'aider avec d\'autres langages.',
            'que puis-je faire avec python': 'Python est très polyvalent, tu peux l\'utiliser pour du développement web, de l\'intelligence artificielle, des scripts, etc.',
            'comment apprendre la programmation': 'Il faut beaucoup pratiquer et comprendre les concepts de base. Commence par des tutoriels et des exercices.',
            'qu\'est-ce qu\'une fonction': 'Une fonction est un bloc de code qui exécute une tâche spécifique et peut être réutilisé.',
            'que sont les boucles en python': 'Les boucles permettent de répéter une tâche plusieurs fois sans avoir à réécrire le même code.',
            'comment écrire une boucle for': 'La syntaxe est : for item in liste: et tu peux ajouter le code à répéter à l\'intérieur.',
            'qu\'est-ce qu\'une variable': 'Une variable est un espace de stockage pour une valeur qui peut changer au cours de l\'exécution du programme.',
            'qu\'est-ce qu\'une classe': 'Une classe est un modèle pour créer des objets. Elle regroupe des attributs et des méthodes.',
            'qu\'est-ce qu\'un objet': 'Un objet est une instance d\'une classe avec des valeurs spécifiques à cet objet.',
            'comment créer une classe en python': 'Tu utilises le mot-clé class suivi du nom de la classe et des méthodes à l\'intérieur.',
            'qu\'est-ce qu\'un dictionnaire en python': 'Un dictionnaire est une collection de paires clé-valeur. Les clés sont uniques.',
            'qu\'est-ce qu\'une liste': 'Une liste est une collection ordonnée d\'éléments qui peuvent être modifiés.',
            'que sont les tuples': 'Les tuples sont similaires aux listes, mais leurs éléments sont immutables.',
            'comment fonctionne un if en Python': 'La syntaxe est : if condition: et le code à exécuter est indenté.',
            'comment vérifier si un nombre est pair': 'Tu peux utiliser l\'opérateur modulo : if number % 2 == 0.',
            'comment créer un fichier en Python': 'Tu peux utiliser la fonction open("nom_fichier", "w") pour créer un fichier.',
            'comment lire un fichier en Python': 'Tu utilises open("nom_fichier", "r") et la méthode read() ou readline() pour lire le fichier.',
            'comment fermer un fichier': 'Après avoir terminé avec un fichier, utilise la méthode close() pour le fermer.',
            'comment créer une fonction en Python': 'Utilise le mot-clé def suivi du nom de la fonction et de ses paramètres.',
            'que sont les exceptions en Python': 'Les exceptions sont des erreurs qui peuvent survenir pendant l\'exécution, que l\'on peut gérer avec try-except.',
            'qu\'est-ce que json': 'JSON (JavaScript Object Notation) est un format léger de stockage et d\'échange de données.',
            'qu\'est-ce que html': 'HTML est un langage de balisage utilisé pour structurer le contenu des pages web.',
            'qu\'est-ce que css': 'CSS est un langage de style utilisé pour décrire la présentation d\'un document HTML.',
            'qu\'est-ce que javascript': 'JavaScript est un langage de programmation utilisé principalement pour créer des pages web interactives.',
            'quelle est la capitale de la france': 'La capitale de la France est Paris.',
            'qui a inventé le téléphone': 'Le téléphone a été inventé par Alexander Graham Bell en 1876.',
            'quel est l\'animal le plus rapide du monde': 'Le guépard est l\'animal terrestre le plus rapide, pouvant atteindre 112 km/h.',
            'combien de continents existe-t-il': 'Il y a 7 continents sur Terre: l\'Asie, l\'Afrique, l\'Amérique, l\'Antarctique, l\'Europe, l\'Océanie et l\'Amérique du Nord.',
            'quel est le plus grand océan du monde': 'Le plus grand océan est l\'océan Pacifique.',
            'quelle est la hauteur de la Tour Eiffel': 'La Tour Eiffel mesure 324 mètres de hauteur.',
            'qui a écrit harry potter': 'Harry Potter a été écrit par J.K. Rowling.',
            'quelle est la langue la plus parlée dans le monde': 'La langue la plus parlée dans le monde est le mandarin, parlé par plus d\'un milliard de personnes.',
            'qui a peint la joconde': 'La Joconde a été peinte par Léonard de Vinci.',
            'quelles sont les couleurs du drapeau de l\'Italie': 'Les couleurs du drapeau italien sont le vert, le blanc et le rouge.',
            'quelle est la distance entre la Terre et la Lune': 'La distance moyenne entre la Terre et la Lune est d\'environ 384 400 kilomètres.',
            'qu\'est-ce qu\'un eclipse solaire': 'Une éclipse solaire se produit lorsque la Lune se trouve entre la Terre et le Soleil, bloquant la lumière du Soleil.',
            'qu\'est-ce que l\'eau': 'L\'eau est une substance liquide composée de deux atomes d\'hydrogène et d\'un atome d\'oxygène.',
            'quel est le point le plus bas sur Terre': 'Le point le plus bas de la Terre est la Mer Morte, située à 430 mètres sous le niveau de la mer.',
            'qu\'est-ce qu\'une étoile': 'Une étoile est une boule de gaz, principalement de l\'hydrogène et de l\'hélium, qui produit de la lumière et de la chaleur par fusion nucléaire.',
            'quelle est la plus grande planète de notre système solaire': 'La plus grande planète de notre système solaire est Jupiter.',
            'combien de pays y a-t-il dans le monde': 'Il y a actuellement 195 pays dans le monde.',
            'qu\'est-ce que la gravité': 'La gravité est la force qui attire les objets vers le centre de la Terre.',
            'quelles sont les parties d\'une plante': 'Les principales parties d\'une plante sont les racines, la tige, les feuilles et les fleurs.',
            'qui a découvert la pénicilline': 'La pénicilline a été découverte par Alexander Fleming en 1928.',
            'qu\'est-ce que la photosynthèse': 'La photosynthèse est le processus par lequel les plantes convertissent la lumière en énergie chimique.',
            'quelles sont les saisons': 'Les quatre saisons sont le printemps, l\'été, l\'automne et l\'hiver.',
            'combien d\'heures y a-t-il dans une journée': 'Il y a 24 heures dans une journée.',
            'quelles sont les parties du corps humain': 'Les principales parties du corps humain sont la tête, le tronc, les bras et les jambes.',
            'quelles sont les unités de mesure du temps': 'Les unités de mesure du temps sont les secondes, minutes, heures, jours, mois et années.',
            'qu\'est-ce qu\'un atome': 'Un atome est la plus petite unité d\'un élément chimique.',
            'qui est albert einstein': 'Albert Einstein était un physicien théoricien, connu pour sa théorie de la relativité.',
            'qu\'est-ce que l\'énergie': 'L\'énergie est la capacité d\'effectuer un travail, elle existe sous plusieurs formes: thermique, cinétique, chimique, etc.',
            'quelles sont les parties d\'un ordinateur': 'Les parties principales d\'un ordinateur sont le processeur, la mémoire RAM, le disque dur, la carte graphique et l\'écran.',
            'comment  fonctionne Internet': 'internet fonctionne grâce à des serveurs qui échangent des données via des câbles et des ondes radio.',
            'qu\'est-ce que l\'intelligence artificielle': 'L\'intelligence artificielle est la capacité d\'une machine à imiter des fonctions cognitives humaines comme l\'apprentissage et la prise de décision.',
            'qui a inventé l\'ordinateur': 'L\'ordinateur a été inventé par Charles Babbage au XIXe siècle, mais il a été largement développé plus tard.',
            'quelles sont les couleurs primaires': 'Les couleurs primaires sont le rouge, le bleu et le jaune.',
            'quelles sont les lois de newton': 'Les lois de Newton décrivent le mouvement des objets, notamment l\'inertie, la force et l\'action/réaction.',
            'qu\'est-ce qu\'un smartphone': 'Un smartphone est un téléphone portable avec un système d\'exploitation permettant de télécharger des applications et d\'accéder à Internet.',
            'comment fonctionne un moteur à combustion': 'Un moteur à combustion fonctionne en brûlant un carburant pour produire de la chaleur et de l\'énergie mécanique.',
            'qu\'est-ce qu\'un réseau social': 'Un réseau social est une plateforme en ligne permettant aux utilisateurs de se connecter, partager et interagir.',
            'qui a découvert l\'amérique': 'L\'Amérique a été "découverte" par Christophe Colomb en 1492, bien que d\'autres peuples y aient déjà vécu bien avant.',
            'quelles sont les langues officielles de l\'ONU': 'Les langues officielles de l\'ONU sont l\'anglais, le français, l\'espagnol, le chinois, le russe et l\'arabe.',
            'qu\'est-ce qu\'un système d\'exploitation': 'Un système d\'exploitation est un logiciel qui gère les ressources matérielles et logicielles d\'un ordinateur.',
            'quel est le plus grand désert du monde': 'Le plus grand désert du monde est le désert de l\'Antarctique.',
            'qu\'est-ce qu\'un volcan': 'Un volcan est une ouverture à la surface de la Terre par laquelle des matériaux comme de la lave, des cendres et des gaz peuvent s\'échappent.',
            'qu\'est-ce que la tectonique des plaques': 'La tectonique des plaques est la théorie expliquant le mouvement des grandes plaques lithosphériques de la Terre.',
            'quelles sont les règles de base du football': 'Le football se joue avec un ballon rond, 11 joueurs par équipe, et l\'objectif est de marquer des buts dans le camp adverse.',
            'quel est le sport le plus populaire': 'Le football est le sport le plus populaire au monde.',
            'qu\'est-ce que la démocratie': 'La démocratie est un système politique où les citoyens ont le pouvoir de choisir leurs représentants par le biais d\'élections.',
            'qu\'est-ce qu\'un parlement': 'Le parlement est une institution législative où sont débattues et votées les lois d\'un pays.',
            'qui est napoléon bonaparte': 'Napoléon Bonaparte était un empereur français, né en 1769 et connu pour ses réformes et ses guerres en Europe.',
            'qu\'est-ce qu\'un mythe': 'Un mythe est une histoire traditionnelle souvent expliquée par des événements surnaturels ou des personnages légendaires.',
            'qui a écrit "les misérables"': 'Les Misérables a été écrit par Victor Hugo.',
            'quelles sont les principales religions du monde': 'Les principales religions sont le christianisme, l\'islam, l\'hindouisme, le bouddhisme et le judaïsme.',
            'quel est le plus grand fleuve du monde': 'Le plus grand fleuve du monde est l\'Amazonie, en termes de volume d\'eau.',
            'quel est le plus grand pays du monde': 'Le plus grand pays du monde par superficie est la Russie.',
            'quel est le plus petit pays du monde': 'Le plus petit pays du monde par superficie est le Vatican.',
            'slt': 'Salut',
            'salut': 'Salut',
            'bjr': 'Bonjour'
        }
    def ask_question(self):
        question = input("Entrez une question: \n")
        if question is not None:
            for keyword, response in self.questions.items():
                if keyword in question.lower():
                    print(response)
        else:
            print('Veulliez entre une question valide')
        
    def main(self):
        while True:
            self.ask_question()
            re_ask = input("Continuer oui/non: ")
            if re_ask.lower() == 'non':
                break

chat = Chatbot()
chat.main()