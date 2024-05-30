import flet as ft
import process as pr

def main(page: ft.Page):
    page.title = "Aplicación Interactiva con Flet"
    
    # Crear un FilePicker
    file_picker = ft.FilePicker(on_result=lambda e: on_file_picked(e))

    # Crear un botón para abrir el FilePicker
    pick_file_button = ft.ElevatedButton(text="Subir Archivo", on_click=lambda e: file_picker.pick_files())

    # Función que se ejecuta cuando se selecciona un archivo
    def on_file_picked(e):
        if e.files:
            # Obtener la ruta del archivo seleccionado
            file_path = e.files[0].path
            gray, median, restricted = pr.autoDetect(file_path)
            # Crear las imágenes
            gray_image = ft.Image(src=gray, width=400, height=400)
            median_image = ft.Image(src=median, width=400, height=400)
            restricted_image = ft.Image(src=restricted, width=400, height=400)
            
            # Crear una fila con las imágenes
            image_row = ft.Row(
                controls=[
                    gray_image,
                    median_image,
                    restricted_image
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
            
            # Agregar la fila a la página
            page.add(image_row)
        else:
            page.add(ft.Text("No se seleccionó ningún archivo."))
        page.update()

     # Añadir el botón y el FilePicker a la página
    page.add(pick_file_button)
    
    # Registrar el FilePicker en la página
    page.overlay.append(file_picker)

  
    # Actualizar la página para mostrar los cambios
    page.update()

# Ejecutar la aplicación Flet
ft.app(target=main)
