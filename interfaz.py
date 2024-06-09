import flet as ft
import process as pr

def main(page: ft.Page):
    page.title = "Aplicación Interactiva con Flet"
    
    # Crear un FilePicker
    file_picker = ft.FilePicker(on_result=lambda e: on_file_picked(e))
    
    # Crear un botón para abrir el FilePicker
    pick_file_button = ft.ElevatedButton(text="Subir Archivo", on_click=lambda e: file_picker.pick_files())
    
    # Crear un contenedor para las imágenes
    image_container = ft.Column()

    # Función que se ejecuta cuando se selecciona un archivo
    def on_file_picked(e):
        if e.files:
            # Limpiar el contenedor de imágenes para evitar imágenes anteriores
            image_container.controls.clear()
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
            
            # Agregar la fila al contenedor de imágenes
            image_container.controls.append(image_row)
        else:
            image_container.controls.append(ft.Text("No se seleccionó ningún archivo."))
        page.update()
    
    # Función para reiniciar la aplicación
    def reset_images(e):
        image_container.controls.clear()
        page.update()
    
    # Crear un botón para reiniciar
    reset_button = ft.ElevatedButton(text="Reiniciar", on_click=reset_images)
    
    # Añadir los botones y el FilePicker a la página
    page.add(pick_file_button)
    page.add(reset_button)
    page.add(image_container)
    
    # Registrar el FilePicker en la página
    page.overlay.append(file_picker)
    
    # Actualizar la página para mostrar los cambios
    page.update()

# Ejecutar la aplicación Flet
ft.app(target=main)
