import os
from controladores import GestorUsuarios, GestorArchivos
from interfaz import VentanaLogin, VentanaPrincipal


def inicializar_sistema():
    print("=" * 50)
    print("Inicializando Sistema de Archivos FAT...")
    print("=" * 50)

    # Crear carpeta de datos si no existe
    carpeta_datos = "datos"
    if not os.path.exists(carpeta_datos):
        os.makedirs(carpeta_datos)
        print(f"✓ Carpeta '{carpeta_datos}/' creada")
    else:
        print(f"✓ Carpeta '{carpeta_datos}/' ya existe")

    # Inicializar gestor de usuarios
    gestor_usuarios = GestorUsuarios()

    # Crear usuario administrador por defecto si no existe
    usuarios_existentes = gestor_usuarios.cargar_usuarios()
    if len(usuarios_existentes) == 0:
        admin_creado = gestor_usuarios.inicializar_usuarios()
        if admin_creado:
            print("✓ Usuario administrador creado (admin/admin)")
    else:
        print(f"✓ Sistema con {len(usuarios_existentes)} usuario(s) registrado(s)")

    # Inicializar gestor de archivos (crea tabla_fat.json si no existe)
    gestor_archivos = GestorArchivos()
    archivos = gestor_archivos.cargar_tabla_fat()
    print(f"✓ Tabla FAT cargada ({len(archivos)} archivo(s))")

    print("=" * 50)
    print("Sistema inicializado correctamente")
    print("=" * 50)
    print()


def main():
    # Inicializar sistema
    inicializar_sistema()

    # Bucle principal para permitir múltiples sesiones
    while True:
        # Mostrar ventana de login
        print("Mostrando ventana de login...")
        ventana_login = VentanaLogin()
        usuario_autenticado = ventana_login.mostrar()

        # Verificar si el usuario se autenticó correctamente
        if usuario_autenticado:
            print(
                f"\n✓ Usuario '{usuario_autenticado.nombre_usuario}' autenticado exitosamente"
            )
            print(
                f"  Tipo: {'Administrador' if usuario_autenticado.es_admin else 'Usuario estándar'}"
            )
            print("\nAbriendo ventana principal...")

            # Mostrar ventana principal
            ventana_principal = VentanaPrincipal(usuario_autenticado)
            cerrar_sesion = ventana_principal.mostrar()

            if cerrar_sesion:
                print("\nSesión cerrada. Volviendo al login...")
                continue  # Volver al inicio del bucle (login)
            else:
                print("\nSesión finalizada. Hasta pronto!")
                break  # Salir del bucle
        else:
            print("\nLogin cancelado. Saliendo del sistema...")
            break  # Salir del bucle

    print("\n" + "=" * 50)
    print("Sistema de Archivos FAT finalizado")
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario")
    except Exception as e:
        print(f"\n\n¡ERROR CRÍTICO!\n{e}")
        import traceback

        traceback.print_exc()
