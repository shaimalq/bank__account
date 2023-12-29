import tkinter as tk
from tkinter import ttk
import json

# Classe Compte: represente les informations de base d'un compte
class Compte:
    def __init__(self, numero, proprietaire, solde, date_ouverture):
        self.numero = numero
        self.proprietaire = proprietaire
        self.solde = solde
        self.date_ouverture = date_ouverture

    def __str__(self):
        return (f"Compte Numéro: {self.numero}, "
                f"Propriétaire: {self.proprietaire}, "
                f"Solde: {self.solde}, "
                f"Date d'Ouverture: {self.date_ouverture}")

class CompteCourant(Compte):
    def __init__(self, numero, proprietaire, solde, date_ouverture, montant_decouvert_autorise):
        super().__init__(numero, proprietaire, solde, date_ouverture)
        self.montant_decouvert_autorise = montant_decouvert_autorise

    def __str__(self):
        return (super().__str__() + 
                f", Montant Découvert Autorisé: {self.montant_decouvert_autorise}")

class CompteEpargne(Compte):
    def __init__(self, numero, proprietaire, solde, date_ouverture, interet):
        super().__init__(numero, proprietaire, solde, date_ouverture)
        self.interet = interet

    def __str__(self):
        return (super().__str__() + 
                f", Intérêt: {self.interet}")

class BankAccountApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Account Creation App")

        # Initialize account number to 0
        self.account_number = tk.IntVar(value=0)
        self.owner_name = tk.StringVar()
        self.initial_balance = tk.StringVar()
        self.account_type = tk.StringVar(value="Courant")
        self.interest_rate = tk.StringVar()
        self.overdraft = tk.StringVar()

        self.setup_accounts_table()
        self.load_accounts()
        self.setup_ui_elements()

    def setup_accounts_table(self):
        self.accounts_table = ttk.Treeview(self.root, columns=("number", "owner", "balance", "type", "interest", "overdraft"), show="headings")
        self.accounts_table.grid(row=7, column=0, columnspan=2)
        self.accounts_table.heading("number", text="#")
        self.accounts_table.heading("owner", text="Propriétaire")
        self.accounts_table.heading("balance", text="Solde Initial")
        self.accounts_table.heading("type", text="Type")
        self.accounts_table.heading("interest", text="Taux Intérêt")
        self.accounts_table.heading("overdraft", text="Montant Découvert")

    def setup_ui_elements(self):
        tk.Label(self.root, text="Numéro:").grid(row=0, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.account_number, state='readonly').grid(row=0, column=1)

        tk.Label(self.root, text="Propriétaire:").grid(row=1, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.owner_name).grid(row=1, column=1)

        tk.Label(self.root, text="Solde Initial:").grid(row=2, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.initial_balance).grid(row=2, column=1)

        tk.Label(self.root, text="Type:").grid(row=3, column=0, sticky="e")
        tk.Radiobutton(self.root, text="Courant", variable=self.account_type, value="Courant").grid(row=3, column=1, sticky="w")
        tk.Radiobutton(self.root, text="Épargne", variable=self.account_type, value="Épargne").grid(row=3, column=1)

        tk.Label(self.root, text="Taux Intérêt:").grid(row=4, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.interest_rate).grid(row=4, column=1)

        tk.Label(self.root, text="Montant Découvert:").grid(row=5, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.overdraft).grid(row=5, column=1)

        tk.Button(self.root, text="Créer Compte", command=self.create_account).grid(row=6, column=1, pady=10)

    def load_accounts(self):
        try:
            with open("accounts.json", "r") as file:
                accounts = json.load(file)
                max_account_number = 0
                for account in accounts:
                    if isinstance(account, dict):
                        self.accounts_table.insert("", "end", values=(
                            account.get("numero", ""),
                            account.get("proprietaire", ""),
                            account.get("solde", ""),
                            account.get("type", ""),
                            account.get("interet", ""),
                            account.get("decouvert", "")
                        ))
                        max_account_number = max(max_account_number, account.get("numero", 0))
                self.account_number.set(max_account_number + 1)
        except FileNotFoundError:
            pass

    def create_account(self):
        account_type = self.account_type.get()
        account = {
            "numero": self.account_number.get(),
            "proprietaire": self.owner_name.get(),
            "solde": self.initial_balance.get(),
            "type": account_type,
            "interet": self.interest_rate.get() if account_type == "Épargne" else "",
            "decouvert": self.overdraft.get() if account_type == "Courant" else ""
        }
        self.accounts_table.insert("", "end", values=(
            account["numero"],
            account["proprietaire"],
            account["solde"],
            account["type"],
            account["interet"],
            account["decouvert"]
        ))
        self.save_accounts(account)
        # Increment the account number for the next account
        self.account_number.set(self.account_number.get() + 1)

    def save_accounts(self, account):
        try:
            with open("accounts.json", "r") as file:
                accounts = json.load(file)
        except FileNotFoundError:
            accounts = []

        accounts.append(account)

        with open("accounts.json", "w") as file:
            json.dump(accounts, file, indent=4)

# Exécution de l'application
root = tk.Tk()
root.geometry("800x600")
app = BankAccountApp(root)
root.mainloop()
