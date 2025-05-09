from app import create_app  # Importa la función que crea la aplicación Flask

app = create_app()  # Crea la instancia de la app con todas las configuraciones, modelos y rutas

if __name__ == "__main__":  # Solo se ejecuta si corres este archivo directamente
    app.run(debug=True)     # Lanza el servidor de desarrollo en modo debug (recarga automática + errores detallados)