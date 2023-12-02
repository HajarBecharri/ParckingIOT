class Car:
    def __init__(self, code_matricule, nom_client, cni_client, date_enregistrement):
        self.code_matricule = code_matricule
        self.nom_client = nom_client
        self.cni_client = cni_client
        self.date_enregistrement = date_enregistrement
    def __init__(self, code_matricule, nom_client, cni_client, date_enregistrement,etat):
        self.code_matricule = code_matricule
        self.nom_client = nom_client
        self.cni_client = cni_client
        self.etat = etat
        self.date_enregistrement = date_enregistrement

class User:
    def __init__(self,email,password) :
        self.email=email
        self.password=password        

class Enregistrement:
    def __init__(self, id, code_matricule, date_entree, date_sortie):
        self.id = id
        self.code_matricule = code_matricule
        self.date_entree = date_entree
        self.date_sortie = date_sortie