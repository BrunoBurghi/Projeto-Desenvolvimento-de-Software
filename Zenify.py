from enum import Enum
import tkinter as tk
from tkinter import messagebox

class Usuario:
    def __init__(self, id, nome, email, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

    def __str__(self):
        return f"Usuário: {self.nome} (ID: {self.id})"

class Categoria(Enum):
    EXERCICIOS = ("Exercícios", 10)
    LAZER = ("Lazer", 3)
    TRABALHO = ("Trabalho", 2)
    SOCIAL = ("Social", 8)
    DOMESTICO = ("Doméstico", 5)

    def __init__(self, descricao, pontuacao_base):
        self.descricao = descricao
        self.pontuacao_base = pontuacao_base

    def __str__(self):
        return self.descricao

    def get_pontuacao_base(self):
        return self.pontuacao_base

class Atividade:
    def __init__(self, id, descricao, Categoria, duracao):
        self.id = id
        self.descricao = descricao
        self.categoria = Categoria
        self.duracao = duracao
        self.impacto_bem_estar = 0
        self.calcular_impacto()

    def calcular_impacto(self):
        # Lógica para calcular o impacto no bem-estar com base na categoria e duração
        self.impacto_bem_estar = int((self.categoria.get_pontuacao_base())) * int(self.duracao)

    def __str__(self):
        return f"{self.descricao} ({self.categoria}): {self.impacto_bem_estar}"

    def get_impacto_bem_estar(self):
        return self.impacto_bem_estar

class Paciente(Usuario):
    def __init__(self, id, nome, email, senha):
        super().__init__(id, nome, email, senha)
        self.atividades = []
        self.historico_pontuacoes = []

    def registrar_atividade(self, atividade):
        self.atividades.append(atividade)

    def gerar_relatorio(self):
        relatorio = RelatorioBemEstar()
        return relatorio.gerar_pontuacao(self.atividades)

    def __str__(self):
        return f"Paciente: {self.nome} (ID: {self.id})"

class Profissional(Usuario):
    def __init__(self, id, nome, email, senha):
        super().__init__(id, nome, email, senha)
        self.pacientes_ativos = []

    def recomendar_atividade(self, paciente, atividade):
        paciente.registrar_atividade(atividade)

    def __str__(self):
        return f"Profissional: {self.nome} (ID: {self.id})"

class Login:
    def iniciar_sessao(self, usuario, email, senha):
        if usuario.email == email and usuario.senha == senha:
            print(f"Sessão iniciada com sucesso para o usuário: {usuario}")
        else:
            print("Falha na autenticação do usuário.")

class RelatorioBemEstar:
    def gerar_pontuacao(self, atividades):
        pontuacao_total = 0
        for atividade in atividades:
            pontuacao_total += atividade.get_impacto_bem_estar()
        return pontuacao_total

    def exibir_relatorio(self, paciente):
        pontuacao_total = 0
        resultado = f"Relatório de Bem-Estar do: {paciente.nome}\n"
        for atividade in paciente.atividades:
            resultado += f"   {atividade.descricao} ({atividade.categoria}): {atividade.get_impacto_bem_estar()}\n"
            pontuacao_total += int(atividade.get_impacto_bem_estar())
        resultado += f"Pontuação Total: {pontuacao_total}"
        return resultado

#Econtrar uma Categoria a partir de uma String
def encontrarCatString(categoria):
    for cat in Categoria:
        if cat.descricao == categoria: return cat

paciente0 = Paciente(0, "n", "e", "s")
profissional0 = Profissional(0, "p", "n", "s")

usuarios = {
    "Paciente": [paciente0],
    "Profissional": [profissional0]
}

#Função para encontrar o usuário a partir do email e seu tipo
def encontrarUsuario(email, tipo):
    for usuario in usuarios[tipo]:
        if usuario.email == email: return True
    return False

# Função de Tela de Login
def tela_login():
    def realizar_login():
        email = entry_email.get()
        senha = entry_senha.get()
        tipo = tipo_selecionado.get()

        if email == "" or senha == "" or tipo == "Tipo de Usuário":
            messagebox.showerror("Erro","Faltou preenchimento de algum campo.")
        else:
            for usuario in usuarios[tipo]:
                if usuario.email == email and usuario.senha == senha:
                    if tipo == "Paciente": tela_principal_paciente(usuario)
                    elif tipo == "Profissional": print("oi")
            messagebox.showerror("Erro","Usuário não encontrado!")
                
    janela_login = tk.Tk()
    janela_login.title("Tela de Login")

    label = tk.Label(janela_login, text="Login", font=("Arial", 14))
    label.pack(pady=20)

    label_email = tk.Label(janela_login, text="Email:")
    label_email.pack(pady=5)
    entry_email = tk.Entry(janela_login, width=30)
    entry_email.pack(pady=5)

    label_senha = tk.Label(janela_login, text="Senha:")
    label_senha.pack(pady=5)
    entry_senha = tk.Entry(janela_login, show="*", width=30)
    entry_senha.pack(pady=5)

    btn_login = tk.Button(janela_login, text="Entrar", width=20, command=realizar_login)
    btn_login.pack(pady=10)

    btn_registrar = tk.Button(janela_login, text="Registrar-se", width=20, command=lambda: tela_registro())
    btn_registrar.pack(pady=10)

    tipo_selecionado = tk.StringVar(janela_login)
    tipo_selecionado.set("Tipo de Usuário")
    tipo_usuario = tk.OptionMenu(janela_login, tipo_selecionado, *usuarios)
    tipo_usuario.pack()


    janela_login.mainloop()

# Função de Tela de Registro
def tela_registro():
    def registrar_usuario():
        nome = entry_nome.get()
        email = entry_email.get()
        senha = entry_senha.get()
        senha_confirmada = entry_senha_confirmar.get()
        tipo = tipo_selecionado.get()

        if email == "" or senha == "" or tipo == "Tipo de Usuário":
            messagebox.showerror("Erro","Faltou preenchimento de algum campo.")
        elif senha != senha_confirmada:
            messagebox.showerror("Erro", "As senhas não coincidem.")
        elif encontrarUsuario(email, tipo):
            messagebox.showerror("Erro", "Esse email já está cadastrado.")
        else:
            if tipo == "Paciente": novo_usuario =  Paciente(len(usuarios[tipo]) + 1, nome,  email, senha) 
            else: novo_usuario =  Profissional(len(usuarios[tipo]) + 1, nome,  email, senha) 
            
            usuarios[tipo].append(novo_usuario)
            messagebox.showinfo("Sucesso", tipo +" registrado com sucesso!")
            janela_registro.destroy()

    janela_registro = tk.Tk()
    janela_registro.title("Tela de Registro")

    label = tk.Label(janela_registro, text="Registrar Usuário", font=("Arial", 14))
    label.pack(pady=20)

    label_nome = tk.Label(janela_registro, text="Nome:")
    label_nome.pack(pady=5)
    entry_nome = tk.Entry(janela_registro, width=30)
    entry_nome.pack(pady=5)

    label_email = tk.Label(janela_registro, text="Email:")
    label_email.pack(pady=5)
    entry_email = tk.Entry(janela_registro, width=30)
    entry_email.pack(pady=5)

    label_senha = tk.Label(janela_registro, text="Senha:")
    label_senha.pack(pady=5)
    entry_senha = tk.Entry(janela_registro, show="*", width=30)
    entry_senha.pack(pady=5)

    label_senha_confirmar = tk.Label(janela_registro, text="Confirmar Senha:")
    label_senha_confirmar.pack(pady=5)
    entry_senha_confirmar = tk.Entry(janela_registro, show="*", width=30)
    entry_senha_confirmar.pack(pady=5)

    tipo_selecionado = tk.StringVar(janela_registro)
    tipo_selecionado.set("Tipo de Usuário")
    tipo_usuario = tk.OptionMenu(janela_registro, tipo_selecionado, *usuarios)
    tipo_usuario.pack()

    btn_registrar = tk.Button(janela_registro, text="Registrar", width=20, command=registrar_usuario)
    btn_registrar.pack(pady=10)

    janela_registro.mainloop()

#Função da Tela Principal do Cliente
def tela_principal_paciente(paciente):
    root = tk.Tk()
    root.title("Tela Principal do Paciente")

    # Botão Registrar Atividade
    btn_registrar_atividade = tk.Button(root, text="Registrar Atividade", command=lambda: tela_registrar_atividade(paciente))
    btn_registrar_atividade.pack(pady=10)

    # Botão Gerar Relatório
    btn_gerar_relatorio = tk.Button(root, text="Gerar Relatório", command=lambda: tela_gerar_relatorio(paciente))
    btn_gerar_relatorio.pack(pady=10)

    # Botão Contatar Profissional
    btn_contatar_profissional = tk.Button(root, text="Contatar Profissional", command=lambda: tela_contatar_profissional(paciente))
    btn_contatar_profissional.pack(pady=10)

    root.mainloop()

#Função para registrar atividade
def tela_registrar_atividade(paciente):
    def registrar():
        descricao = entry_descricao.get()
        categoria = encontrarCatString(categoria_var.get())
        duracao = entry_duracao.get()

        if descricao and categoria != "Selecione a categoria da sua Atividade!" and duracao:
            nova_atividade = Atividade(len(paciente.atividades)+1, descricao, categoria, duracao)
            paciente.atividades.append(nova_atividade)
            messagebox.showinfo("Sucesso", "Atividade registrada com sucesso!")
            print(nova_atividade)
            janela_registrar_atividade.destroy()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")

    janela_registrar_atividade = tk.Tk()
    janela_registrar_atividade.title("Registrar Atividade")

    label = tk.Label(janela_registrar_atividade, text="Registrar Atividade", font=("Arial", 14))
    label.pack(pady=20)

    label_descricao = tk.Label(janela_registrar_atividade, text="Descrição da Atividade:")
    label_descricao.pack(pady=5)
    entry_descricao = tk.Entry(janela_registrar_atividade, width=30)
    entry_descricao.pack(pady=5)

    label_categoria = tk.Label(janela_registrar_atividade, text="Categoria da Atividade:")
    label_categoria.pack(pady=5)

    categoria_var = tk.StringVar(janela_registrar_atividade)
    categoria_var.set("Selecione a categoria da sua Atividade!")
    dropdown_categoria = tk.OptionMenu(janela_registrar_atividade, categoria_var, *Categoria)
    dropdown_categoria.pack(pady=5)

    label_duracao = tk.Label(janela_registrar_atividade, text="Duração da Atividade (em minutos):")
    label_duracao.pack(pady=5)
    entry_duracao = tk.Entry(janela_registrar_atividade, width=30)
    entry_duracao.pack(pady=5)

    btn_registrar = tk.Button(janela_registrar_atividade, text="Registrar", width=20, command=registrar)
    btn_registrar.pack(pady=10)

    janela_registrar_atividade.mainloop()

#Função para gerar relatório
def tela_gerar_relatorio(paciente):
    atividades_usuario = paciente.atividades
    
    if not atividades_usuario:
        messagebox.showerror("Erro", "Você não registrou nenhuma atividade.")
        return

    relatorio = RelatorioBemEstar()

    messagebox.showinfo("Relatório", relatorio.exibir_relatorio(paciente))

# Função Tela Contatar Profissional
def tela_contatar_profissional(paciente):
    def associar_profissional(paciente, profissional):
        profissional.pacientes_ativos.append(paciente)
        messagebox.showinfo("Sucesso", "Profissional associado com sucesso!")

    janela_contatar_profissional = tk.Tk()
    janela_contatar_profissional.title("Contatar Profissional")

    label = tk.Label(janela_contatar_profissional, text="Escolha um Profissional", font=("Arial", 14))
    label.pack(pady=20)

    for profissional in usuarios["Profissional"]:
        if len(profissional.pacientes_ativos) <= 5:
            btn_profissional = tk.Button(
                janela_contatar_profissional, 
                text=profissional.nome,
                width=30,
                command=lambda p=profissional: associar_profissional(paciente, p)
            )
            btn_profissional.pack(pady=5)

    janela_contatar_profissional.mainloop()

tela_login()