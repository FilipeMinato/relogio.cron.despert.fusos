import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pytz  # Para trabalhar com fusos horários internacionais
import time
import winsound  # Para emitir som no alarme (somente no Windows)

# ==============================
# FUSOS HORÁRIOS DAS CIDADES
# ==============================
# Dicionário com cidades e seus respectivos fusos horários do módulo pytz
cidades = {
    "Tóquio 🇯🇵": "Asia/Tokyo",
    "Londres 🇬🇧": "Europe/London",
    "Berlim 🇩🇪": "Europe/Berlin",
    "São Paulo 🇧🇷": "America/Sao_Paulo"
}

# =====================================
# FUNÇÃO: Atualiza os relógios na tela
# =====================================
def atualizar_relogios():
    """
    Atualiza o horário de cada cidade e exibe na interface.
    Chama também a verificação do alarme.
    """
    for cidade, fuso_nome in cidades.items():
        fuso = pytz.timezone(fuso_nome)
        hora = datetime.now(fuso).strftime('%H:%M:%S')
        labels_relogio[cidade].config(text=hora)

    verificar_alarme()  # Verifica se o alarme deve tocar
    janela.after(1000, atualizar_relogios)  # Repetição a cada 1 segundo

# ===========================================
# FUNÇÕES DO CRONÔMETRO COM MILÉSIMOS
# ===========================================

def iniciar_cronometro():
    """
    Inicia o cronômetro, guardando o tempo de início ajustado.
    """
    global cronometro_rodando, tempo_inicio
    if not cronometro_rodando:
        cronometro_rodando = True
        tempo_inicio = time.perf_counter() - tempo_cronometro
        atualizar_cronometro()

def pausar_cronometro():
    """
    Pausa o cronômetro e salva o tempo decorrido até o momento.
    """
    global cronometro_rodando, tempo_cronometro
    if cronometro_rodando:
        cronometro_rodando = False
        tempo_cronometro = time.perf_counter() - tempo_inicio

def zerar_cronometro():
    """
    Zera o cronômetro e atualiza o texto da tela.
    """
    global tempo_cronometro, tempo_inicio
    tempo_cronometro = 0
    tempo_inicio = time.perf_counter()
    label_cronometro.config(text="00:00:00.000")

def atualizar_cronometro():
    """
    Atualiza o cronômetro na tela em tempo real (a cada 10 milissegundos).
    """
    if cronometro_rodando:
        tempo_decorrido = time.perf_counter() - tempo_inicio

        # Converte tempo total em horas, minutos, segundos e milésimos
        horas = int(tempo_decorrido // 3600)
        minutos = int((tempo_decorrido % 3600) // 60)
        segundos = int(tempo_decorrido % 60)
        milesimos = int((tempo_decorrido - int(tempo_decorrido)) * 1000)

        label_cronometro.config(text=f"{horas:02d}:{minutos:02d}:{segundos:02d}.{milesimos:03d}")
        janela.after(10, atualizar_cronometro)  # Atualiza a cada 10ms

# =========================
# FUNÇÕES DO DESPERTADOR
# =========================

alarme_ativado = False  # Estado do alarme (ativado ou não)
hora_alarme = None      # Horário configurado para tocar

def ativar_alarme():
    """
    Ativa o alarme com hora e minuto informados pelo usuário.
    """
    global alarme_ativado, hora_alarme
    try:
        h = int(entrada_hora.get())
        m = int(entrada_minuto.get())
        hora_alarme = f"{h:02d}:{m:02d}"
        alarme_ativado = True
        messagebox.showinfo("Alarme", f"Alarme definido para {hora_alarme}")
    except:
        messagebox.showerror("Erro", "Hora inválida. Digite números válidos.")

def verificar_alarme():
    """
    Verifica se o horário atual corresponde ao alarme e, se sim, toca um som e mostra alerta.
    """
    global alarme_ativado
    if alarme_ativado:
        agora = datetime.now().strftime("%H:%M")
        if agora == hora_alarme:
            alarme_ativado = False  # Desativa após tocar
            try:
                winsound.Beep(1000, 1000)  # Emite som de 1000Hz por 1 segundo
            except:
                pass
            messagebox.showinfo("⏰ Alarme", f"É hora! {hora_alarme}")

# ===================================
# INICIALIZAÇÃO DA INTERFACE GRÁFICA
# ===================================
print("Iniciando aplicativo...")
time.sleep(1)  # Espera 1 segundo antes de abrir a janela

janela = tk.Tk()
janela.title("Relógio Mundial, Cronômetro com Milésimos e Despertador")

# ================================
# SEÇÃO DOS RELÓGIOS INTERNACIONAIS
# ================================
frame_relogios = tk.Frame(janela)
frame_relogios.pack(pady=10)

labels_relogio = {}  # Armazena os labels de cada cidade para atualizar depois

for cidade in cidades:
    frame = tk.Frame(frame_relogios)
    frame.pack(pady=3)

    # Nome da cidade
    tk.Label(frame, text=cidade, font=("Arial", 18)).pack(side=tk.LEFT, padx=5)

    # Horário da cidade (atualizado dinamicamente)
    labels_relogio[cidade] = tk.Label(frame, font=("Arial", 18), fg="blue")
    labels_relogio[cidade].pack(side=tk.LEFT, padx=10)

# =======================
# SEÇÃO DO CRONÔMETRO
# =======================
label_cronometro = tk.Label(janela, text="00:00:00.000", font=("Courier", 28), fg="red")
label_cronometro.pack(pady=10)

frame_cron = tk.Frame(janela)
frame_cron.pack()

tk.Button(frame_cron, text="Iniciar", width=12, command=iniciar_cronometro).grid(row=0, column=0, padx=5)
tk.Button(frame_cron, text="Pausar", width=12, command=pausar_cronometro).grid(row=0, column=1, padx=5)
tk.Button(frame_cron, text="Zerar", width=12, command=zerar_cronometro).grid(row=0, column=2, padx=5)

# =======================
# SEÇÃO DO DESPERTADOR
# =======================
frame_alarme = tk.Frame(janela)
frame_alarme.pack(pady=10)

tk.Label(frame_alarme, text="⏰ Despertador:", font=("Arial", 14)).grid(row=0, column=0, columnspan=5)

tk.Label(frame_alarme, text="Hora:").grid(row=1, column=0)
entrada_hora = tk.Entry(frame_alarme, width=5)
entrada_hora.grid(row=1, column=1)

tk.Label(frame_alarme, text="Min:").grid(row=1, column=2)
entrada_minuto = tk.Entry(frame_alarme, width=5)
entrada_minuto.grid(row=1, column=3)

tk.Button(frame_alarme, text="Ativar Alarme", command=ativar_alarme).grid(row=1, column=4, padx=10)

# =======================
# VARIÁVEIS INICIAIS
# =======================
cronometro_rodando = False  # Indica se o cronômetro está rodando
tempo_cronometro = 0        # Tempo decorrido até a pausa
tempo_inicio = 0            # Momento em que foi iniciado

# Inicia os relógios e a interface
atualizar_relogios()
janela.mainloop()
