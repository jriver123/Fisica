"""
app.py
──────
Clase Aplicacion: ventana principal que ensambla todos los
paneles y maneja las acciones del usuario (Calcular / Limpiar).
"""
 
import tkinter as tk
from tkinter import messagebox
 
from constantes import Constantes
from fisica     import MotorFisico
from paneles    import PanelObjetivo, PanelCargas, PanelResultados, PanelGrafica
 
 
class Aplicacion:
    """
    Ventana principal del programa.
 
    Responsabilidades:
      · Construir el layout general (encabezado, columnas)
      · Instanciar cada panel y ubicarlo en la ventana
      · Conectar los botones con las acciones correspondientes
      · Orquestar el flujo: leer datos → calcular → mostrar
    """
 
    def __init__(self, root):
        self._root = root
        C = Constantes
 
        root.title("Principio de Superposición – Ley de Coulomb")
        root.configure(bg=C.DARK_BG)
        root.resizable(True, True)
        root.minsize(860, 640)
 
        self._construir_interfaz()
 
    # ── Construcción del layout ─────────────────────────────────
    def _construir_interfaz(self):
        C = Constantes
 
        # Encabezado
        encabezado = tk.Frame(self._root, bg=C.DARK_BG)
        encabezado.pack(fill="x", padx=20, pady=(18, 4))
 
        tk.Label(
            encabezado,
            text="⚡  PRINCIPIO DE SUPERPOSICIÓN",
            font=C.TITULO, fg=C.ACCENT, bg=C.DARK_BG
        ).pack(side="left")
 
        tk.Label(
            encabezado,
            text="Ley de Coulomb",
            font=("Courier New", 10), fg=C.TEXT_MUTED, bg=C.DARK_BG
        ).pack(side="left", padx=12, pady=4)
 
        # Separador
        tk.Frame(self._root, bg=C.BORDER, height=1).pack(
            fill="x", padx=20, pady=4
        )
 
        # Panel principal de dos columnas
        principal = tk.Frame(self._root, bg=C.DARK_BG)
        principal.pack(fill="both", expand=True, padx=20, pady=6)
 
        # Columna izquierda: entradas + resultados
        izquierda = tk.Frame(principal, bg=C.DARK_BG, width=460)
        izquierda.pack(side="left", fill="both", expand=False, padx=(0, 12))
        izquierda.pack_propagate(False)
 
        self._panel_objetivo   = PanelObjetivo(izquierda)
        self._panel_cargas     = PanelCargas(izquierda)
        self._construir_botones(izquierda)
        self._panel_resultados = PanelResultados(izquierda)
 
        # Columna derecha: gráfica
        derecha = tk.Frame(
            principal, bg=C.CARD_BG,
            highlightbackground=C.BORDER, highlightthickness=1
        )
        derecha.pack(side="left", fill="both", expand=True)
 
        self._panel_grafica = PanelGrafica(derecha)
 
    def _construir_botones(self, contenedor):
        C = Constantes
        fila = tk.Frame(contenedor, bg=C.DARK_BG)
        fila.pack(fill="x", pady=10)
 
        tk.Button(
            fila,
            text="⚡  CALCULAR FUERZA NETA",
            font=("Courier New", 11, "bold"),
            fg=C.DARK_BG, bg=C.ACCENT,
            activebackground="#388bfd",
            relief="flat", bd=0, padx=18, pady=8, cursor="hand2",
            command=self._calcular
        ).pack(side="left", padx=(0, 8))
 
        tk.Button(
            fila,
            text="↺  Limpiar",
            font=C.SMALL,
            fg=C.TEXT_MUTED, bg=C.INPUT_BG,
            activebackground=C.BORDER,
            relief="flat", bd=0, padx=10, pady=8, cursor="hand2",
            command=self._limpiar
        ).pack(side="left")
 
    # ── Acciones ────────────────────────────────────────────────
    def _calcular(self):
        """
        Flujo completo al presionar ⚡ CALCULAR:
          1. Leer carga objetivo
          2. Verificar que haya cargas fuente
          3. Leer cargas fuente
          4. Calcular (física pura, sin UI)
          5. Mostrar resultados y actualizar gráfica
        """
        # 1. Leer carga objetivo
        try:
            q_obj, x_obj, y_obj = self._panel_objetivo.obtener_valores()
        except ValueError as e:
            messagebox.showerror("Error – Carga objetivo", str(e))
            return
 
        # 2. Verificar que haya al menos una carga fuente
        if not self._panel_cargas.hay_cargas():
            messagebox.showwarning(
                "Sin cargas fuente",
                "Agrega al menos una carga fuente con  ＋ Agregar carga."
            )
            return
 
        # 3. Leer cargas fuente
        try:
            cargas_fuente = self._panel_cargas.obtener_todas()
        except ValueError as e:
            messagebox.showerror("Error – Cargas fuente", str(e))
            return
 
        # 4. Calcular (delegado al MotorFisico)
        try:
            Fx, Fy, magnitud, angulo, detalles = MotorFisico.fuerza_neta(
                cargas_fuente, q_obj, (x_obj, y_obj)
            )
        except ValueError as e:
            messagebox.showerror("Error físico", str(e))
            return
 
        # 5. Presentar resultados y gráfica
        self._panel_resultados.mostrar(Fx, Fy, magnitud, angulo, detalles)
        self._panel_grafica.dibujar(
            cargas_fuente, q_obj, (x_obj, y_obj), Fx, Fy, detalles
        )
 
    def _limpiar(self):
        """Delega la limpieza a cada panel."""
        self._panel_objetivo.limpiar()
        self._panel_cargas.limpiar()
        self._panel_resultados.limpiar()
        self._panel_grafica.limpiar()
 
    # ── Arranque ────────────────────────────────────────────────
    def iniciar(self, geometria="1050x720"):
        """Establece el tamaño inicial y entra al bucle de eventos."""
        self._root.geometry(geometria)
        self._root.mainloop()