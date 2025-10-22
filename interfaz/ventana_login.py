import tkinter as tk
from tkinter import messagebox
from controladores import GestorUsuarios


class VentanaLogin:
    def __init__(self):
        self.gestor_usuarios = GestorUsuarios()
        self.usuario_autenticado = None

        # Crear ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Archivos FAT - Login")
        self.ventana.geometry("400x300")
        self.ventana.resizable(False, False)

        # Centrar ventana en pantalla
        self.centrar_ventana()

        # Crear interfaz
        self.crear_widgets()

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = self.ventana.winfo_width()
        alto = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_widgets(self):
        # Frame principal
        frame_principal = tk.Frame(self.ventana, padx=20, pady=20)
        frame_principal.pack(expand=True)

        # Título
        titulo = tk.Label(
            frame_principal, text="Sistema de Archivos FAT", font=("Arial", 16, "bold")
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Label y Entry para usuario
        label_usuario = tk.Label(frame_principal, text="Usuario:", font=("Arial", 10))
        label_usuario.grid(row=1, column=0, sticky="e", padx=(0, 10), pady=5)

        self.entry_usuario = tk.Entry(frame_principal, width=25, font=("Arial", 10))
        self.entry_usuario.grid(row=1, column=1, pady=5)
        self.entry_usuario.focus()

        # Label y Entry para contraseña
        label_password = tk.Label(
            frame_principal, text="Contraseña:", font=("Arial", 10)
        )
        label_password.grid(row=2, column=0, sticky="e", padx=(0, 10), pady=5)

        self.entry_password = tk.Entry(
            frame_principal, width=25, show="*", font=("Arial", 10)
        )
        self.entry_password.grid(row=2, column=1, pady=5)

        # Bind Enter key para login
        self.entry_password.bind("<Return>", lambda event: self.iniciar_sesion())

        # Frame para botones
        frame_botones = tk.Frame(frame_principal)
        frame_botones.grid(row=3, column=0, columnspan=2, pady=(20, 0))

        # Botón Iniciar Sesión
        boton_login = tk.Button(
            frame_botones,
            text="Iniciar Sesión",
            command=self.iniciar_sesion,
            width=15,
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            cursor="hand2",
        )
        boton_login.pack(side=tk.LEFT, padx=5)

        # Botón Registrar
        boton_registrar = tk.Button(
            frame_botones,
            text="Registrar Usuario",
            command=self.registrar_usuario,
            width=15,
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            cursor="hand2",
        )
        boton_registrar.pack(side=tk.LEFT, padx=5)

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get()

        # Validar campos vacíos
        if not usuario or not password:
            messagebox.showwarning(
                "Campos vacíos", "Por favor ingrese usuario y contraseña"
            )
            return

        # Autenticar
        usuario_autenticado = self.gestor_usuarios.autenticar(usuario, password)

        if usuario_autenticado:
            self.usuario_autenticado = usuario_autenticado
            messagebox.showinfo(
                "Login exitoso", f"Bienvenido {usuario_autenticado.nombre_usuario}"
            )
            self.ventana.destroy()  # Cerrar el loop y continuar en main
        else:
            messagebox.showerror(
                "Error de autenticación", "Usuario o contraseña incorrectos"
            )
            self.entry_password.delete(0, tk.END)
            self.entry_password.focus()

    def registrar_usuario(self):
        # Crear ventana de registro
        ventana_registro = tk.Toplevel(self.ventana)
        ventana_registro.title("Registrar Usuario")
        ventana_registro.geometry("350x250")
        ventana_registro.resizable(False, False)
        ventana_registro.transient(self.ventana)
        ventana_registro.grab_set()

        # Frame principal
        frame = tk.Frame(ventana_registro, padx=20, pady=20)
        frame.pack(expand=True)

        # Título
        titulo = tk.Label(frame, text="Nuevo Usuario", font=("Arial", 12, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Usuario
        tk.Label(frame, text="Usuario:", font=("Arial", 10)).grid(
            row=1, column=0, sticky="e", padx=(0, 10), pady=5
        )
        entry_nuevo_usuario = tk.Entry(frame, width=20, font=("Arial", 10))
        entry_nuevo_usuario.grid(row=1, column=1, pady=5)
        entry_nuevo_usuario.focus()

        # Contraseña
        tk.Label(frame, text="Contraseña:", font=("Arial", 10)).grid(
            row=2, column=0, sticky="e", padx=(0, 10), pady=5
        )
        entry_nueva_password = tk.Entry(frame, width=20, show="*", font=("Arial", 10))
        entry_nueva_password.grid(row=2, column=1, pady=5)

        # Confirmar contraseña
        tk.Label(frame, text="Confirmar:", font=("Arial", 10)).grid(
            row=3, column=0, sticky="e", padx=(0, 10), pady=5
        )
        entry_confirmar_password = tk.Entry(
            frame, width=20, show="*", font=("Arial", 10)
        )
        entry_confirmar_password.grid(row=3, column=1, pady=5)

        def guardar_usuario():
            nuevo_usuario = entry_nuevo_usuario.get().strip()
            nueva_password = entry_nueva_password.get()
            confirmar_password = entry_confirmar_password.get()

            # Validaciones
            if not nuevo_usuario or not nueva_password:
                messagebox.showwarning("Campos vacíos", "Complete todos los campos")
                return

            if nueva_password != confirmar_password:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                entry_nueva_password.delete(0, tk.END)
                entry_confirmar_password.delete(0, tk.END)
                return

            if len(nueva_password) < 4:
                messagebox.showwarning(
                    "Contraseña débil", "La contraseña debe tener al menos 4 caracteres"
                )
                return

            # Registrar usuario
            exito, mensaje = self.gestor_usuarios.registrar_usuario(
                nuevo_usuario, nueva_password
            )

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                ventana_registro.destroy()
            else:
                messagebox.showerror("Error", mensaje)

        # Botones
        frame_botones = tk.Frame(frame)
        frame_botones.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        boton_guardar = tk.Button(
            frame_botones,
            text="Registrar",
            command=guardar_usuario,
            width=12,
            font=("Arial", 9),
            bg="#4CAF50",
            fg="white",
        )
        boton_guardar.pack(side=tk.LEFT, padx=5)

        boton_cancelar = tk.Button(
            frame_botones,
            text="Cancelar",
            command=ventana_registro.destroy,
            width=12,
            font=("Arial", 9),
        )
        boton_cancelar.pack(side=tk.LEFT, padx=5)

        # Bind Enter para guardar
        entry_confirmar_password.bind("<Return>", lambda e: guardar_usuario())

    def mostrar(self):
        # Muestra la ventana y retorna el usuario autenticado
        self.ventana.mainloop()
        return self.usuario_autenticado
