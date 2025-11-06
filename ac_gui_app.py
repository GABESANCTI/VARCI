# ac_gui_app.py

import tkinter as tk
from tkinter import ttk, messagebox
import cmath
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importa as funções de cálculo do outro arquivo
try:
    from complex_ac_calculator import Z_serie, Z_paralelo, obter_Z_complexa_direta, calcular_potencias
except ImportError:
    messagebox.showerror("Erro de Módulo", "O arquivo 'complex_ac_calculator.py' não foi encontrado. Certifique-se de que ele está no mesmo diretório.")


class CircuitoApp:
    def __init__(self, root):
        self.root = root
        root.title("Analisador de Circuitos CA Monofásicos RLC")
        root.geometry("1100x700")

        self.impedancias = {} 
        self.z_counter = 1
        
        # --- Configuração do Layout Principal ---
        
        self.input_frame = ttk.Frame(root, padding="10")
        self.input_frame.grid(row=0, column=0, sticky=(tk.W, tk.N, tk.S), padx=10, pady=10)
        
        self.output_frame = ttk.Frame(root, padding="10")
        self.output_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        self._setup_input_widgets()
        self._setup_output_widgets()

    # --- SETUP DA INTERFACE DE ENTRADA (Item A: Entrada de Parâmetros) ---
    def _setup_input_widgets(self):
        # 1. ENTRADA DA FONTE -------------------------------------------
        fonte_group = ttk.LabelFrame(self.input_frame, text=" Fonte de Tensão (V_fonte) ")
        fonte_group.grid(row=0, column=0, pady=10, padx=5, sticky='ew')
        
        ttk.Label(fonte_group, text="Módulo (V_rms):").grid(row=0, column=0, padx=5, pady=2, sticky='w')
        self.V_mag_entry = ttk.Entry(fonte_group, width=10)
        self.V_mag_entry.insert(0, "220")  # Valor inicial coerente
        self.V_mag_entry.grid(row=0, column=1, padx=5, pady=2, sticky='e')
        
        ttk.Label(fonte_group, text="Ângulo (graus):").grid(row=1, column=0, padx=5, pady=2, sticky='w')
        self.V_phase_entry = ttk.Entry(fonte_group, width=10)
        self.V_phase_entry.insert(0, "0")
        self.V_phase_entry.grid(row=1, column=1, padx=5, pady=2, sticky='e')

        # 2. CRIAÇÃO DE IMPEDÂNCIA BASE ---------------------------------
        z_base_group = ttk.LabelFrame(self.input_frame, text=" Criar Z Base (R, XL, XC) ")
        z_base_group.grid(row=1, column=0, pady=10, padx=5, sticky='ew')
        
        ttk.Label(z_base_group, text="Nome:").grid(row=0, column=0, padx=5, pady=2, sticky='w')
        self.z_name_entry = ttk.Entry(z_base_group, width=10)
        self.z_name_entry.insert(0, f"Z{self.z_counter}")
        self.z_name_entry.grid(row=0, column=1, padx=5, pady=2, sticky='e')

        ttk.Label(z_base_group, text="R (\u03A9):").grid(row=1, column=0, padx=5, pady=2, sticky='w')
        self.R_entry = ttk.Entry(z_base_group, width=10)
        self.R_entry.insert(0, "5") # Valor inicial coerente
        self.R_entry.grid(row=1, column=1, padx=5, pady=2, sticky='e')

        ttk.Label(z_base_group, text="XL (\u03A9):").grid(row=2, column=0, padx=5, pady=2, sticky='w')
        self.XL_entry = ttk.Entry(z_base_group, width=10)
        self.XL_entry.insert(0, "15") # Valor inicial coerente
        self.XL_entry.grid(row=2, column=1, padx=5, pady=2, sticky='e')

        ttk.Label(z_base_group, text="XC (\u03A9):").grid(row=3, column=0, padx=5, pady=2, sticky='w')
        self.XC_entry = ttk.Entry(z_base_group, width=10)
        self.XC_entry.insert(0, "10") # Valor inicial coerente
        self.XC_entry.grid(row=3, column=1, padx=5, pady=2, sticky='e')
        
        ttk.Button(z_base_group, text="Adicionar Z", command=self._add_impedance).grid(
            row=4, column=0, columnspan=2, pady=5)

        # 3. ASSOCIAÇÃO DE IMPEDÂNCIAS ----------------------------------
        z_assoc_group = ttk.LabelFrame(self.input_frame, text=" Associar (Série / Paralelo) ")
        z_assoc_group.grid(row=2, column=0, pady=10, padx=5, sticky='ew')
        
        ttk.Label(z_assoc_group, text="Nomes (Z1, Z2, ...):").grid(row=0, column=0, padx=5, pady=2, sticky='w')
        self.assoc_names_entry = ttk.Entry(z_assoc_group, width=15)
        self.assoc_names_entry.grid(row=0, column=1, padx=5, pady=2, sticky='e')
        
        ttk.Label(z_assoc_group, text="Nome Resultado:").grid(row=1, column=0, padx=5, pady=2, sticky='w')
        self.assoc_result_entry = ttk.Entry(z_assoc_group, width=15)
        self.assoc_result_entry.insert(0, "Z_Eq")
        self.assoc_result_entry.grid(row=1, column=1, padx=5, pady=2, sticky='e')
        
        ttk.Button(z_assoc_group, text="Série", command=lambda: self._associate_impedances("serie")).grid(
            row=2, column=0, pady=5, padx=5)
        ttk.Button(z_assoc_group, text="Paralelo", command=lambda: self._associate_impedances("paralelo")).grid(
            row=2, column=1, pady=5, padx=5)

        # 4. BOTÃO DE CÁLCULO FINAL -------------------------------------
        ttk.Label(self.input_frame, text="Nome da Z Total:").grid(row=3, column=0, padx=5, pady=2, sticky='w')
        self.z_total_name_entry = ttk.Entry(self.input_frame, width=15)
        self.z_total_name_entry.insert(0, "Z_Eq")
        self.z_total_name_entry.grid(row=4, column=0, padx=5, pady=2, sticky='ew')
        
        ttk.Button(self.input_frame, text="⚙️ CALCULAR TUDO E PLOTAR", command=self._calculate_total_circuit).grid(
            row=5, column=0, pady=10, sticky='ew')


    # --- SETUP DA INTERFACE DE SAÍDA ---
    def _setup_output_widgets(self):
        # 1. Área de Texto para Resultados (B, C, D, E)
        self.results_text = tk.Text(self.output_frame, height=15, width=60, wrap='word')
        self.results_text.grid(row=0, column=0, sticky='nsew', pady=5)
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)

        # 2. Área de Gráficos (F e G) - Abas
        self.notebook = ttk.Notebook(self.output_frame)
        self.notebook.grid(row=1, column=0, sticky='nsew', pady=10)
        self.output_frame.grid_rowconfigure(1, weight=3)

        self.fasor_tab = ttk.Frame(self.notebook)
        self.potencia_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.fasor_tab, text="Diagrama Fasorial [G]")
        self.notebook.add(self.potencia_tab, text="Triângulo de Potências [F]")

        # Inicialização do Matplotlib para o Fasorial
        self.fig_fasor = plt.Figure(figsize=(5, 4), dpi=100)
        self.canvas_fasor = FigureCanvasTkAgg(self.fig_fasor, master=self.fasor_tab)
        self.canvas_fasor.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Inicialização do Matplotlib para o Triângulo de Potências
        self.fig_potencia = plt.Figure(figsize=(5, 4), dpi=100)
        self.canvas_potencia = FigureCanvasTkAgg(self.fig_potencia, master=self.potencia_tab)
        self.canvas_potencia.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    # --- MÉTODOS DE LÓGICA ---
    
    def _add_impedance(self):
        # Item B: Cálculo da Impedância Equivalente (Z base)
        try:
            nome = self.z_name_entry.get().strip()
            # Pega valor do campo ou usa 0.0 se estiver vazio
            R = float(self.R_entry.get() or 0.0)
            XL = float(self.XL_entry.get() or 0.0)
            XC = float(self.XC_entry.get() or 0.0)
            
            if not nome: raise ValueError("Nome não pode ser vazio.")
            if nome in self.impedancias: raise ValueError(f"Nome '{nome}' já existe.")
            
            Z = obter_Z_complexa_direta(R, XL, XC)
            self.impedancias[nome] = Z
            
            self.results_text.insert(tk.END, f"✔️ Criada Z: {nome} = {Z:.4f} Ω\n")
            self.z_counter += 1
            self.z_name_entry.delete(0, tk.END)
            self.z_name_entry.insert(0, f"Z{self.z_counter}")
            
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", f"Detalhe: {e}")

    def _associate_impedances(self, tipo):
        # Item B: Cálculo da Impedância Equivalente (Série/Paralelo)
        try:
            nomes = [n.strip() for n in self.assoc_names_entry.get().split(',')]
            nome_resultado = self.assoc_result_entry.get().strip()
            
            if not nome_resultado or not all(nomes):
                raise ValueError("Preencha todos os campos de associação.")

            impedancias_para_combinar = [self.impedancias[n] for n in nomes]

            if tipo == 'serie':
                Z_resultante = Z_serie(impedancias_para_combinar)
            else: # paralelo
                Z_resultante = Z_paralelo(impedancias_para_combinar)
            
            self.impedancias[nome_resultado] = Z_resultante
            
            self.results_text.insert(tk.END, f"✔️ Associada Z: {nome_resultado} ({tipo}) = {Z_resultante:.4f} Ω\n")
            self.assoc_names_entry.delete(0, tk.END)
            
        except KeyError:
            messagebox.showerror("Erro de Associação", "Um ou mais nomes de impedância não foram encontrados.")
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", str(e))

    def _calculate_total_circuit(self):
        # Executa os Itens C, D, E, F, G
        try:
            V_mag = float(self.V_mag_entry.get() or 0)
            V_fase_rad = math.radians(float(self.V_phase_entry.get() or 0))
            V_fonte = cmath.rect(V_mag, V_fase_rad)
            
            nome_z_total = self.z_total_name_entry.get().strip()
            Z_total = self.impedancias.get(nome_z_total)
            
            if Z_total is None:
                 messagebox.showerror("Erro", f"A impedância total '{nome_z_total}' não foi criada.")
                 return

            # CÁLCULOS
            I_total = V_fonte / Z_total # Item C: Cálculo da Corrente Total
            S_total, P_ativa, Q_reativa, S_aparente, fator_potencia = \
                calcular_potencias(V_fonte, I_total, Z_total) # Itens D, E: Cálculo das Potências e FP

            # ATUALIZAÇÃO DO DISPLAY DE RESULTADOS
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "====== ANÁLISE TOTAL DO CIRCUITO ======\n")
            
            Z_mag = abs(Z_total); Z_fase_deg = math.degrees(cmath.phase(Z_total))
            I_mag = abs(I_total); I_fase_deg = math.degrees(cmath.phase(I_total))
            
            self.results_text.insert(tk.END, f"Z Total: {Z_total:.4f} Ω\nZ Polar: |{Z_mag:.4f} Ω| \u2220 {Z_fase_deg:.4f}°\n")
            self.results_text.insert(tk.END, f"I Total: |{I_mag:.4f} A| \u2220 {I_fase_deg:.4f}°\n\n")
            self.results_text.insert(tk.END, f"P Ativa: {P_ativa:.4f} W\nQ Reativa: {Q_reativa:.4f} VAR\nS Aparente: {S_aparente:.4f} VA\n")
            self.results_text.insert(tk.END, f"Fator de Potência (FP): {fator_potencia:.4f}\n")
            
            # GERAÇÃO DE GRÁFICOS
            self._plot_fasorial(V_fonte, I_total, nome_z_total) # Item G
            self._plot_potencias(P_ativa, Q_reativa, S_total, nome_z_total) # Item F
            
        except Exception as e:
            messagebox.showerror("Erro de Cálculo", f"Ocorreu um erro: {e}")

    # ITEM F: CONSTRUÇÃO DO TRIÂNGULO DE POTÊNCIAS
    def _plot_potencias(self, P_ativa, Q_reativa, S_total, nome_z_total):
        self.fig_potencia.clear()
        ax = self.fig_potencia.add_subplot(111)

        ax.plot([0, P_ativa], [0, 0], 'b-', linewidth=2, label=f'P = {P_ativa:.2f} W')
        ax.plot([P_ativa, P_ativa], [0, Q_reativa], 'g-', linewidth=2, label=f'Q = {Q_reativa:.2f} VAR')
        S_mag = abs(S_total)
        S_fase_deg = math.degrees(cmath.phase(S_total))
        ax.plot([0, P_ativa], [0, Q_reativa], 'r--', linewidth=2, label=f'S = {S_mag:.2f} VA  {S_fase_deg:.2f}°')
        
        head_size = S_mag * 0.05 if S_mag > 0 else 1
        ax.arrow(0, 0, P_ativa, Q_reativa, head_width=head_size, head_length=head_size, fc='r', ec='r', alpha=0.5, length_includes_head=True)

        ax.set_title(f'Triângulo de Potências ({nome_z_total})')
        ax.set_xlabel('P (W)'); ax.set_ylabel('Q (VAR)')
        ax.grid(True); ax.axhline(0, color='black', linewidth=0.5); ax.axvline(0, color='black', linewidth=0.5)
        ax.set_aspect('equal', adjustable='box')
        ax.legend(loc='upper right')
        self.canvas_potencia.draw()

    # ITEM G: CONSTRUÇÃO DO DIAGRAMA FASORIAL (CORRIGIDO SEM RÓTULO DE ESCALA)
    def _plot_fasorial(self, V_fonte, I_total, nome_z_total):
        self.fig_fasor.clear()
        ax = self.fig_fasor.add_subplot(111, projection='polar') 
        
        V_mag = abs(V_fonte); V_fase_rad = cmath.phase(V_fonte)
        I_mag = abs(I_total); I_fase_rad = cmath.phase(I_total)

        # 1. Cálculo da Escala Adaptativa (mantido para visualização)
        I_plot_mag = 0
        if V_mag > 0 and I_mag > 0:
            scale_factor = V_mag / (I_mag + V_mag) 
            I_plot_mag = I_mag * scale_factor
        elif V_mag > 0:
            I_plot_mag = I_mag
        
        # 2. Plot Fasor V
        ax.plot([0, V_fase_rad], [0, V_mag], marker='o', color='blue', linewidth=2,
                label=f'V_fonte: {V_mag:.2f}V  {math.degrees(V_fase_rad):.2f}°')

        # 3. Plot Fasor I (escalado, mas o rótulo é o valor real)
        i_label = f'I_total: {I_mag:.2f}A  {math.degrees(I_fase_rad):.2f}°'

        ax.plot([0, I_fase_rad], [0, I_plot_mag], marker='^', color='red', linewidth=2,
                label=i_label)

        ax.set_title(f'Diagrama Fasorial (V e I) - {nome_z_total}', va='bottom')
        ax.legend(loc='lower left', bbox_to_anchor=(1.05, 0.5))
        ax.set_theta_zero_location("E")
        ax.set_theta_direction(-1)
        self.canvas_fasor.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = CircuitoApp(root)
    root.mainloop()