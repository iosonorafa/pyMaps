import tkinter as tk
from tkinter import messagebox, scrolledtext
import folium
import ast  # Para convertir la cadena de coordenadas en una lista


def trazar_coordenadas():
    try:
        # Obtener el texto del TextArea y convertirlo en una lista de coordenadas
        coordenadas_texto = text_area.get("1.0", tk.END).strip()

        # Convertir la cadena de texto a una lista utilizando ast.literal_eval
        coordenadas_lista = ast.literal_eval(coordenadas_texto)

        # Validar que la lista tenga un número par de elementos
        if len(coordenadas_lista) % 2 != 0:
            raise ValueError("Número impar de valores ingresados.")

        # Convertir la lista en pares de coordenadas (latitud, longitud)
        coordenadas = [(float(coordenadas_lista[i]), float(coordenadas_lista[i + 1])) for i in
                       range(0, len(coordenadas_lista), 2)]

        if not coordenadas:
            messagebox.showerror("Error", "No hay coordenadas para trazar.")
            return

        # Crear un mapa centrado en la primera coordenada
        mapa = folium.Map(location=coordenadas[0], zoom_start=10)

        # Añadir marcadores para cada coordenada
        for lat, lon in coordenadas:
            folium.Marker(location=[lat, lon]).add_to(mapa)

        # Añadir una línea que conecta las coordenadas
        folium.PolyLine(coordenadas, color='blue', weight=2.5, opacity=1).add_to(mapa)

        # Guardar el mapa en un archivo HTML
        mapa.save('ruta_mapa.html')
        messagebox.showinfo("Información", "El mapa ha sido guardado como 'ruta_mapa.html'.")

    except ValueError as e:
        messagebox.showerror("Error", f"Error en las coordenadas: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")


def limpiar_texto():
    text_area.delete("1.0", tk.END)


# Crear la ventana principal
root = tk.Tk()
root.title("Trazar Coordenadas")

# Crear un frame para el área de texto
frame_text_area = tk.Frame(root)
frame_text_area.pack(pady=10, padx=10)

# Crear y configurar el área de texto para ingresar coordenadas
label_text_area = tk.Label(frame_text_area, text="Ingrese las coordenadas (en formato [latitud, longitud, ...]):")
label_text_area.pack(pady=5)

text_area = scrolledtext.ScrolledText(frame_text_area, wrap=tk.WORD, width=60, height=10, bg='white', fg='black',
                                      insertbackground='black', highlightthickness=1, highlightbackground='black')
text_area.pack(pady=5)

# Crear botones para trazar coordenadas y limpiar el área de texto
button_trazar = tk.Button(root, text="Trazar Coordenadas", command=trazar_coordenadas)
button_trazar.pack(pady=5)

button_limpiar = tk.Button(root, text="Limpiar", command=limpiar_texto)
button_limpiar.pack(pady=5)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
