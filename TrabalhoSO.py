import random
import queue

class Processo:
    def __init__(self, pid, tempo_execucao, prioridade):
        self.pid = pid
        self.tempo_execucao = tempo_execucao
        self.prioridade = prioridade
        self.tempo_restante = tempo_execucao

    def __lt__(self, other):
        return self.prioridade < other.prioridade

    def __str__(self):
        return f"Processo {self.pid} (Prioridade {self.prioridade}): Tempo Restante: {self.tempo_restante}"

    def executar(self, quantum):
        tempo_usado = min(quantum, self.tempo_restante)
        self.tempo_restante -= tempo_usado
        print(f"Processo {self.pid} executado por {tempo_usado} unidades. Tempo restante: {self.tempo_restante} unidades.")
        return self.tempo_restante == 0  # RETORNA TRUE SE TERMINOU

def escalonamento_prioridade(processos, quantum, tempo_aumento_prioridade):
    tempo_atual = 0
    filas = [queue.Queue() for _ in range(4)]  # FILas de prioridade

    # ADICIONA PROCESSOS
    for processo in processos:
        filas[processo.prioridade].put(processo)

    print("\n=== INÍCIO DO ESCALONAMENTO POR PRIORIDADE ===\n")
    while any(not fila.empty() for fila in filas):
        for prioridade, fila in enumerate(filas):
            if not fila.empty():
                processo = fila.get()
                terminado = processo.executar(quantum)
                tempo_atual += quantum

                if terminado:
                    print(f"Processo {processo.pid} finalizado no tempo {tempo_atual}")
                else:
                    fila.put(processo)  # RETORNA PROCESSO PARA A FILA
                print(f"Tempo Atual: {tempo_atual} unidades")

                # AUMENTA PRIORIDADE
                if tempo_atual % tempo_aumento_prioridade == 0:
                    print(f"\n=== AUMENTO DE PRIORIDADE NO TEMPO {tempo_atual} ===")
                    for prio, fila_prio in enumerate(filas):
                        processos_na_fila = []
                        while not fila_prio.empty():
                            p = fila_prio.get()
                            if p.prioridade > 0:  #AUMENTA PRIORIDADE, SE PUDER
                                p.prioridade -= 1
                                print(f"Processo {p.pid} movido para prioridade {p.prioridade}.")
                                filas[p.prioridade].put(p)  # MOVE ENTRE FILAS
                            else:
                                processos_na_fila.append(p)
                        for p in processos_na_fila:
                            fila_prio.put(p)
                    print("=" * 40)

    print("\n=== TODOS OS PROCESSOS FORAM FINALIZADOS ===")

def obter_dados_processos():
    num_processos = int(input("Número de processos: "))
    processos = []
    for i in range(num_processos):
        tempo_execucao = int(input(f"Tempo de execução do processo {i}: "))
        prioridade = int(input(f"Prioridade do processo {i} (0-3): "))
        processos.append(Processo(i, tempo_execucao, prioridade))

    quantum = int(input("Quantum: "))
    tempo_aumento_prioridade = int(input("Tempo para aumento de prioridade: "))
    
    return processos, quantum, tempo_aumento_prioridade

def gerar_dados_aleatorios(num_processos=5):
    processos = []
    for i in range(num_processos):
        tempo_execucao = random.randint(1, 10)
        prioridade = random.randint(0, 3)
        processos.append(Processo(i, tempo_execucao, prioridade))

    quantum = random.randint(1, 3)
    tempo_aumento_prioridade = random.randint(5, 15)

    return processos, quantum, tempo_aumento_prioridade

def exibir_processos(processos):
    print("\n=== PROCESSOS A SEREM ESCALONADOS ===")
    print(f"{'ID':<10} {'Tempo Execução':<15} {'Prioridade':<10}")
    print("-" * 40)
    for p in processos:
        print(f"{p.pid:<10} {p.tempo_execucao:<15} {p.prioridade:<10}")
    print("-" * 40)

if __name__ == "__main__":
    escolha = input("Deseja fornecer dados manualmente (s/n): ").lower()
    
    if escolha == 's':
        processos, quantum, tempo_aumento_prioridade = obter_dados_processos()
    else:
        processos, quantum, tempo_aumento_prioridade = gerar_dados_aleatorios()

    exibir_processos(processos)
    escalonamento_prioridade(processos, quantum, tempo_aumento_prioridade)
