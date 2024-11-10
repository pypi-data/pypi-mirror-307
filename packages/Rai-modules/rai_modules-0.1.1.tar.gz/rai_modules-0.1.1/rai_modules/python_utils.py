class Chatbot:
    def __init__(self):
        self.questions = {
            'bonjour': 'Bonjour comment allez-vous?',
            'je vais bien': 'Je suis content pour vous',
            'corrige mon code:': 'D\'accord je vais essayer',
            'for keyword, response in': 'Il faut faire for keyword, response in ton_dictionnaire.items()'
        }
    def ask_question(self):
        question = input("Entrez une question: \n")
        if question is not None:
            for keyword, response in self.questions.items():
                if keyword in question.lower():
                    print(response)
                else:
                    print('Je ne comprends pas')
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