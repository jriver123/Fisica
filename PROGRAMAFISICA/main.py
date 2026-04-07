"""
main.py
───────
Punto de entrada del programa.
Ejecutar:
    python main.py
 
Dependencias opcionales (para la gráfica):
    pip install matplotlib numpy
"""
 
import tkinter as tk
from app import Aplicacion
 
 
def main():
    """Crea la ventana raíz, instancia la Aplicacion y la inicia."""
    root = tk.Tk()
    app  = Aplicacion(root)
    app.iniciar("1050x720")
 
 
if __name__ == "__main__":
    main()
 