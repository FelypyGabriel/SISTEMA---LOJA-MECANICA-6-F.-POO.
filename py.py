import mysql.connector

class Cliente:

    @staticmethod
    def deletar(cliente_id):
        conn = Conexao.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT nome FROM cliente WHERE id_cliente = %s", (cliente_id,))
            cliente = cursor.fetchone()

            if not cliente:
                print("Cliente não encontrado.")
                return

            confirmar = input(f"Deletar {cliente[0]} e todos os veículos vinculados? (s/n): ").lower()
            if confirmar != "s":
                print("Operação cancelada.")
                return

            # Excluir peças vinculadas às ordens de serviço
            cursor.execute("""
                DELETE po FROM peca_ordem po
                JOIN ordem_servico os ON po.id_ordem = os.id_ordem
                JOIN veiculo v ON os.id_veiculo = v.id_veiculo
                WHERE v.id_cliente = %s
            """, (cliente_id,))

            # Excluir ordens de serviço
            cursor.execute("""
                DELETE os FROM ordem_servico os
                JOIN veiculo v ON os.id_veiculo = v.id_veiculo
                WHERE v.id_cliente = %s
            """, (cliente_id,))

            # Excluir veículos
            cursor.execute("DELETE FROM veiculo WHERE id_cliente = %s", (cliente_id,))

            # Excluir cliente
            cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (cliente_id,))

            conn.commit()
            print("Cliente e todos os dados vinculados foram deletados com sucesso.")

        except mysql.connector.Error as err:
            print(f"Erro ao deletar: {err}")
        finally:
            cursor.close()
            conn.close()


class Conexao:
    @staticmethod
    def conectar():
        return mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="",
            database="dbMecanica"
        )


class Cliente:
    def __init__(self, nome, telefone, email, endereco):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.endereco = endereco

    def salvar(self):
        conn = Conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Cliente WHERE email = %s", (self.email,))
        if cursor.fetchone():
            print("Cliente já cadastrado com esse e-mail.")
        else:
            cursor.execute("""
                INSERT INTO Cliente (nome, telefone, email, endereco)
                VALUES (%s, %s, %s, %s)
            """, (self.nome, self.telefone, self.email, self.endereco))
            conn.commit()
            print("Cliente cadastrado com sucesso.")
        cursor.close()
        conn.close()

    @staticmethod
    def listar():
        conn = Conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Cliente")
        clientes = cursor.fetchall()
        print("\n--- Lista de Clientes ---")
        for cliente in clientes:
            print(cliente)
        cursor.close()
        conn.close()

    @staticmethod
    def deletar(cliente_id):
        conn = Conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM Cliente WHERE id_cliente = %s", (cliente_id,))
        cliente = cursor.fetchone()
        if not cliente:
            print("Cliente não encontrado.")
        else:
            confirmar = input(f"Deletar {cliente[0]} e todos os veículos vinculados? (s/n): ").lower()
            if confirmar == "s":
                try:
                    # Deleta veículos do cliente antes
                    cursor.execute("DELETE FROM Veiculo WHERE id_cliente = %s", (cliente_id,))
                    # Deleta o cliente
                    cursor.execute("DELETE FROM Cliente WHERE id_cliente = %s", (cliente_id,))
                    conn.commit()
                    print("Cliente e veículos deletados com sucesso.")
                except mysql.connector.Error as erro:
                    print(f"Erro ao deletar: {erro}")
        cursor.close()
        conn.close()

    @staticmethod
    def atualizar(cliente_id, novo_nome=None, novo_telefone=None):
        conn = Conexao.conectar()
        cursor = conn.cursor()
        if novo_nome:
            cursor.execute("UPDATE Cliente SET nome = %s WHERE id_cliente = %s", (novo_nome, cliente_id))
        if novo_telefone:
            cursor.execute("UPDATE Cliente SET telefone = %s WHERE id_cliente = %s", (novo_telefone, cliente_id))
        conn.commit()
        print("Dados atualizados.")
        cursor.close()
        conn.close()

    @staticmethod
    def buscar_por_nome(parte_nome):
        conn = Conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Cliente WHERE nome LIKE %s", (f"%{parte_nome}%",))
        resultados = cursor.fetchall()
        for cliente in resultados:
            print(cliente)
        cursor.close()
        conn.close()

    @staticmethod
    def listar_ordens(cliente_id):
        conn = Conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT os.id_ordem, os.descricao_servico, os.data_entrada
            FROM ordem_servico os
            JOIN veiculo v ON os.id_veiculo = v.id_veiculo
            JOIN cliente c ON v.id_cliente = c.id_cliente
            WHERE c.id_cliente = %s
        """, (cliente_id,))
        ordens = cursor.fetchall()
        if ordens:
            print(f"\n--- Ordens de serviço do cliente {cliente_id} ---")
            for ordem in ordens:
                print(ordem)
        else:
            print("Nenhuma ordem encontrada para este cliente.")
        cursor.close()
        conn.close()


# MENU EXEMPLO
def menu():
    while True:
        print("\n--- MENU CLIENTE ---")
        print("1 - Cadastrar Cliente")
        print("2 - Listar Clientes")
        print("3 - Deletar Cliente")
        print("4 - Atualizar Cliente")
        print("5 - Buscar por Nome")
        print("6 - Ordens de Serviço do Cliente")
        print("0 - Sair")
        opcao = input("Opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            telefone = input("Telefone: ")
            email = input("Email: ")
            endereco = input("Endereço: ")
            Cliente(nome, telefone, email, endereco).salvar()

        elif opcao == "2":
            Cliente.listar()

        elif opcao == "3":
            try:
                cliente_id = int(input("ID do cliente a deletar: "))
                Cliente.deletar(cliente_id)
            except ValueError:
                print("ID inválido.")

        elif opcao == "4":
            try:
                cliente_id = int(input("ID do cliente: "))
                novo_nome = input("Novo nome (Enter para manter): ")
                novo_telefone = input("Novo telefone (Enter para manter): ")
                Cliente.atualizar(cliente_id, novo_nome or None, novo_telefone or None)
            except ValueError:
                print("ID inválido.")

        elif opcao == "5":
            nome = input("Parte do nome a buscar: ")
            Cliente.buscar_por_nome(nome)

        elif opcao == "6":
            try:
                cliente_id = int(input("ID do cliente: "))
                Cliente.listar_ordens(cliente_id)
            except ValueError:
                print("ID inválido.")

        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()