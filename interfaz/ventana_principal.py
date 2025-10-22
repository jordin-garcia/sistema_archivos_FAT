import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from controladores import GestorArchivos, GestorPermisos, GestorUsuarios


class VentanaPrincipal:
    def __init__(self, usuario):
        self.usuario = usuario
        self.gestor_archivos = GestorArchivos()
        self.gestor_permisos = GestorPermisos()
        self.gestor_usuarios = GestorUsuarios()

        self.archivo_seleccionado = None
        self.modo_papelera = False
        self.cerrar_sesion_activo = False

        # Crear ventana principal
        self.ventana = tk.Tk()
        self.ventana.title(
            f"Sistema de Archivos FAT - Usuario: {usuario.nombre_usuario}"
        )
        self.ventana.geometry("900x600")

        # Crear interfaz
        self.crear_menu()
        self.crear_widgets()
        self.actualizar_lista_archivos()

        # Protocolo de cierre
        self.ventana.protocol("WM_DELETE_WINDOW", self.salir)

    def crear_menu(self):
        menubar = tk.Menu(self.ventana)
        self.ventana.config(menu=menubar)

        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Crear Archivo", command=self.crear_archivo)
        menu_archivo.add_command(label="Abrir Archivo", command=self.abrir_archivo)
        menu_archivo.add_command(
            label="Modificar Archivo", command=self.modificar_archivo
        )
        menu_archivo.add_command(
            label="Eliminar Archivo", command=self.eliminar_archivo
        )
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
        menu_archivo.add_command(label="Salir", command=self.salir)

        # Menú Permisos
        menu_permisos = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Permisos", menu=menu_permisos)
        menu_permisos.add_command(
            label="Asignar Permisos", command=self.asignar_permisos
        )
        menu_permisos.add_command(label="Ver Permisos", command=self.ver_permisos)

        # Menú Papelera
        menu_papelera = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Papelera", menu=menu_papelera)
        menu_papelera.add_command(label="Ver Papelera", command=self.ver_papelera)
        menu_papelera.add_command(
            label="Recuperar Archivo", command=self.recuperar_archivo
        )
        menu_papelera.add_command(
            label="Eliminar Permanente", command=self.eliminar_permanente
        )
        menu_papelera.add_command(
            label="Volver a Archivos", command=self.volver_archivos
        )

    def crear_widgets(self):
        # Frame principal con dos paneles
        frame_principal = tk.Frame(self.ventana)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Panel izquierdo - Lista de archivos
        frame_izquierdo = tk.Frame(frame_principal, width=300)
        frame_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))

        # Label del panel izquierdo
        self.label_lista = tk.Label(
            frame_izquierdo, text="Archivos Disponibles", font=("Arial", 11, "bold")
        )
        self.label_lista.pack(pady=(0, 5))

        # Listbox con scrollbar
        frame_listbox = tk.Frame(frame_izquierdo)
        frame_listbox.pack(fill=tk.BOTH, expand=True)

        scrollbar_lista = tk.Scrollbar(frame_listbox)
        scrollbar_lista.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_archivos = tk.Listbox(
            frame_listbox,
            yscrollcommand=scrollbar_lista.set,
            font=("Arial", 10),
            selectmode=tk.SINGLE,
        )
        self.listbox_archivos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_lista.config(command=self.listbox_archivos.yview)

        # Bind para selección
        self.listbox_archivos.bind("<<ListboxSelect>>", self.on_seleccionar_archivo)
        self.listbox_archivos.bind("<Double-Button-1>", lambda e: self.abrir_archivo())

        # Panel derecho - Contenido y metadatos
        frame_derecho = tk.Frame(frame_principal)
        frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Label del panel derecho
        tk.Label(
            frame_derecho, text="Contenido del Archivo", font=("Arial", 11, "bold")
        ).pack(pady=(0, 5))

        # Área de texto con scrollbar
        self.text_contenido = scrolledtext.ScrolledText(
            frame_derecho, wrap=tk.WORD, font=("Courier", 10), state=tk.DISABLED
        )
        self.text_contenido.pack(fill=tk.BOTH, expand=True)

        # Barra inferior - Información del usuario
        frame_inferior = tk.Frame(self.ventana, bg="#f0f0f0", height=30)
        frame_inferior.pack(side=tk.BOTTOM, fill=tk.X)

        tipo_usuario = "Administrador" if self.usuario.es_admin else "Usuario"
        self.label_usuario = tk.Label(
            frame_inferior,
            text=f"Usuario: {self.usuario.nombre_usuario} ({tipo_usuario})",
            bg="#f0f0f0",
            font=("Arial", 9),
        )
        self.label_usuario.pack(side=tk.LEFT, padx=10, pady=5)

    def actualizar_lista_archivos(self):
        self.listbox_archivos.delete(0, tk.END)

        if self.modo_papelera:
            archivos = self.gestor_archivos.listar_archivos(incluir_papelera=True)
            archivos = [a for a in archivos if a.en_papelera]
        else:
            archivos = self.gestor_archivos.listar_archivos(incluir_papelera=False)

        for archivo in archivos:
            self.listbox_archivos.insert(tk.END, archivo.nombre_archivo)

    def on_seleccionar_archivo(self, event):
        seleccion = self.listbox_archivos.curselection()
        if seleccion:
            nombre_archivo = self.listbox_archivos.get(seleccion[0])
            self.archivo_seleccionado = self.gestor_archivos.obtener_archivo_por_nombre(
                nombre_archivo, incluir_papelera=self.modo_papelera
            )

    def crear_archivo(self):
        # Diálogo para nombre
        nombre = simpledialog.askstring("Crear Archivo", "Nombre del archivo:")
        if not nombre:
            return

        # Ventana para contenido
        ventana_contenido = tk.Toplevel(self.ventana)
        ventana_contenido.title("Contenido del Archivo")
        ventana_contenido.geometry("500x500")
        ventana_contenido.transient(self.ventana)
        ventana_contenido.grab_set()

        tk.Label(
            ventana_contenido,
            text=f"Contenido de '{nombre}':",
            font=("Arial", 10, "bold"),
        ).pack(pady=10)

        text_contenido = scrolledtext.ScrolledText(
            ventana_contenido, wrap=tk.WORD, font=("Courier", 10)
        )
        text_contenido.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))
        text_contenido.focus()

        def guardar():
            contenido = text_contenido.get("1.0", tk.END).strip()
            exito, mensaje = self.gestor_archivos.crear_archivo(
                nombre, contenido, self.usuario.nombre_usuario
            )

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                ventana_contenido.destroy()
                self.actualizar_lista_archivos()
            else:
                messagebox.showerror("Error", mensaje)

        frame_botones = tk.Frame(ventana_contenido)
        frame_botones.pack(pady=10)

        tk.Button(
            frame_botones,
            text="Guardar",
            command=guardar,
            width=12,
            bg="#4CAF50",
            fg="white",
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame_botones, text="Cancelar", command=ventana_contenido.destroy, width=12
        ).pack(side=tk.LEFT, padx=5)

    def abrir_archivo(self):
        if not self.archivo_seleccionado:
            messagebox.showwarning("Sin selección", "Seleccione un archivo primero")
            return

        # Verificar permisos de lectura
        if not self.gestor_permisos.tiene_permiso_lectura(
            self.archivo_seleccionado, self.usuario
        ):
            messagebox.showerror(
                "Sin permisos", "No tiene permisos de lectura sobre este archivo"
            )
            return

        # Abrir archivo
        archivo_fat, contenido = self.gestor_archivos.abrir_archivo(
            self.archivo_seleccionado.nombre_archivo
        )

        if archivo_fat:
            # Mostrar metadatos y contenido
            self.text_contenido.config(state=tk.NORMAL)
            self.text_contenido.delete("1.0", tk.END)

            # Insertar metadatos
            self.text_contenido.insert(tk.END, f"{'=' * 50}\n")
            self.text_contenido.insert(
                tk.END, f"Archivo: {archivo_fat.nombre_archivo}\n"
            )
            self.text_contenido.insert(
                tk.END, f"Propietario: {archivo_fat.propietario}\n"
            )
            self.text_contenido.insert(
                tk.END, f"Caracteres: {archivo_fat.cantidad_caracteres}\n"
            )
            self.text_contenido.insert(
                tk.END, f"Creación: {archivo_fat.fecha_creacion[:19]}\n"
            )
            self.text_contenido.insert(
                tk.END, f"Modificación: {archivo_fat.fecha_modificacion[:19]}\n"
            )
            self.text_contenido.insert(tk.END, f"{'=' * 50}\n\n")

            # Insertar contenido
            self.text_contenido.insert(tk.END, contenido)
            self.text_contenido.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", "No se pudo abrir el archivo")

    def modificar_archivo(self):
        if not self.archivo_seleccionado:
            messagebox.showwarning("Sin selección", "Seleccione un archivo primero")
            return

        # Verificar permisos de escritura
        if not self.gestor_permisos.tiene_permiso_escritura(
            self.archivo_seleccionado, self.usuario
        ):
            messagebox.showerror(
                "Sin permisos", "No tiene permisos de escritura sobre este archivo"
            )
            return

        # Obtener contenido actual
        archivo_fat, contenido_actual = self.gestor_archivos.abrir_archivo(
            self.archivo_seleccionado.nombre_archivo
        )

        if not archivo_fat:
            messagebox.showerror("Error", "No se pudo abrir el archivo")
            return

        # Ventana para editar contenido
        ventana_editar = tk.Toplevel(self.ventana)
        ventana_editar.title(f"Modificar: {archivo_fat.nombre_archivo}")
        ventana_editar.geometry("500x500")
        ventana_editar.transient(self.ventana)
        ventana_editar.grab_set()

        tk.Label(
            ventana_editar,
            text=f"Modificar '{archivo_fat.nombre_archivo}':",
            font=("Arial", 10, "bold"),
        ).pack(pady=10)

        text_editar = scrolledtext.ScrolledText(
            ventana_editar, wrap=tk.WORD, font=("Courier", 10)
        )
        text_editar.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))
        text_editar.insert("1.0", contenido_actual)
        text_editar.focus()

        def guardar_cambios():
            nuevo_contenido = text_editar.get("1.0", tk.END).strip()
            exito, mensaje = self.gestor_archivos.modificar_archivo(
                archivo_fat.nombre_archivo, nuevo_contenido
            )

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                ventana_editar.destroy()
                self.actualizar_lista_archivos()
                # Actualizar vista si el archivo está abierto
                self.abrir_archivo()
            else:
                messagebox.showerror("Error", mensaje)

        frame_botones = tk.Frame(ventana_editar)
        frame_botones.pack(pady=10)

        tk.Button(
            frame_botones,
            text="Guardar",
            command=guardar_cambios,
            width=12,
            bg="#4CAF50",
            fg="white",
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame_botones, text="Cancelar", command=ventana_editar.destroy, width=12
        ).pack(side=tk.LEFT, padx=5)

    def eliminar_archivo(self):
        if not self.archivo_seleccionado:
            messagebox.showwarning("Sin selección", "Seleccione un archivo primero")
            return

        # Verificar permisos de escritura
        if not self.gestor_permisos.tiene_permiso_escritura(
            self.archivo_seleccionado, self.usuario
        ):
            messagebox.showerror(
                "Sin permisos", "No tiene permisos para eliminar este archivo"
            )
            return

        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Mover '{self.archivo_seleccionado.nombre_archivo}' a la papelera?",
        )

        if respuesta:
            exito, mensaje = self.gestor_archivos.eliminar_archivo(
                self.archivo_seleccionado.nombre_archivo
            )

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_lista_archivos()
                self.archivo_seleccionado = None
                self.text_contenido.config(state=tk.NORMAL)
                self.text_contenido.delete("1.0", tk.END)
                self.text_contenido.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Error", mensaje)

    def asignar_permisos(self):
        if not self.archivo_seleccionado:
            messagebox.showwarning("Sin selección", "Seleccione un archivo primero")
            return

        # Verificar que sea propietario o admin
        if (
            self.archivo_seleccionado.propietario != self.usuario.nombre_usuario
            and not self.usuario.es_admin
        ):
            messagebox.showerror(
                "Sin autorización",
                "Solo el propietario o administrador pueden asignar permisos",
            )
            return

        # Ventana de asignación de permisos
        ventana_permisos = tk.Toplevel(self.ventana)
        ventana_permisos.title(f"Permisos: {self.archivo_seleccionado.nombre_archivo}")
        ventana_permisos.geometry("400x300")
        ventana_permisos.transient(self.ventana)
        ventana_permisos.grab_set()

        frame = tk.Frame(ventana_permisos, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            frame,
            text=f"Asignar permisos en:\n'{self.archivo_seleccionado.nombre_archivo}'",
            font=("Arial", 10, "bold"),
        ).pack(pady=(0, 15))

        # Seleccionar usuario
        tk.Label(frame, text="Usuario:", font=("Arial", 9)).pack(anchor="w")

        usuarios = self.gestor_usuarios.obtener_todos_usuarios()
        # Filtrar propietario
        usuarios = [u for u in usuarios if u != self.archivo_seleccionado.propietario]

        var_usuario = tk.StringVar()
        if usuarios:
            var_usuario.set(usuarios[0])

        combo_usuarios = tk.OptionMenu(frame, var_usuario, *usuarios)
        combo_usuarios.config(width=25)
        combo_usuarios.pack(pady=(0, 15))

        # Checkboxes para permisos
        var_lectura = tk.BooleanVar()
        var_escritura = tk.BooleanVar()

        tk.Checkbutton(
            frame, text="Permiso de Lectura", variable=var_lectura, font=("Arial", 9)
        ).pack(anchor="w", pady=5)

        tk.Checkbutton(
            frame,
            text="Permiso de Escritura",
            variable=var_escritura,
            font=("Arial", 9),
        ).pack(anchor="w", pady=5)

        def guardar_permisos():
            usuario_destino = var_usuario.get()
            lectura = var_lectura.get()
            escritura = var_escritura.get()

            if not usuario_destino:
                messagebox.showwarning("Sin usuario", "Seleccione un usuario")
                return

            # Cargar todos los archivos primero
            archivos = self.gestor_archivos.listar_archivos(incluir_papelera=True)

            # Encontrar el archivo en la lista
            archivo_a_modificar = None
            for archivo in archivos:
                if archivo.nombre_archivo == self.archivo_seleccionado.nombre_archivo:
                    archivo_a_modificar = archivo
                    break

            if not archivo_a_modificar:
                messagebox.showerror("Error", "Archivo no encontrado")
                return

            # Asignar permisos
            exito, mensaje = self.gestor_permisos.asignar_permiso(
                archivo_a_modificar,
                usuario_destino,
                lectura,
                escritura,
                self.usuario,
            )

            if exito:
                # Guardar la tabla FAT con los cambios
                self.gestor_archivos.guardar_tabla_fat(archivos)
                messagebox.showinfo("Éxito", mensaje)
                ventana_permisos.destroy()
            else:
                messagebox.showerror("Error", mensaje)

        frame_botones = tk.Frame(frame)
        frame_botones.pack(pady=20)

        tk.Button(
            frame_botones,
            text="Asignar",
            command=guardar_permisos,
            width=12,
            bg="#4CAF50",
            fg="white",
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame_botones, text="Cancelar", command=ventana_permisos.destroy, width=12
        ).pack(side=tk.LEFT, padx=5)

    def ver_permisos(self):
        if not self.archivo_seleccionado:
            messagebox.showwarning("Sin selección", "Seleccione un archivo primero")
            return

        permisos_lista = self.gestor_permisos.listar_usuarios_con_permisos(
            self.archivo_seleccionado
        )

        mensaje = f"Permisos de '{self.archivo_seleccionado.nombre_archivo}':\n\n"
        for usuario, permisos in permisos_lista:
            es_propietario = permisos.get("propietario", False)
            lectura = "✓" if permisos.get("lectura", False) else "✗"
            escritura = "✓" if permisos.get("escritura", False) else "✗"

            if es_propietario:
                mensaje += f"• {usuario} (Propietario) - Total\n"
            else:
                mensaje += f"• {usuario} - Lectura: {lectura}, Escritura: {escritura}\n"

        messagebox.showinfo("Permisos del Archivo", mensaje)

    def ver_papelera(self):
        self.modo_papelera = True
        self.label_lista.config(text="Papelera de Reciclaje")
        self.actualizar_lista_archivos()
        self.text_contenido.config(state=tk.NORMAL)
        self.text_contenido.delete("1.0", tk.END)
        self.text_contenido.config(state=tk.DISABLED)

    def volver_archivos(self):
        self.modo_papelera = False
        self.label_lista.config(text="Archivos Disponibles")
        self.actualizar_lista_archivos()

    def recuperar_archivo(self):
        if not self.modo_papelera:
            messagebox.showinfo("Modo Papelera", "Active el modo papelera primero")
            return

        if not self.archivo_seleccionado:
            messagebox.showwarning(
                "Sin selección", "Seleccione un archivo de la papelera"
            )
            return

        respuesta = messagebox.askyesno(
            "Confirmar", f"¿Recuperar '{self.archivo_seleccionado.nombre_archivo}'?"
        )

        if respuesta:
            exito, mensaje = self.gestor_archivos.recuperar_archivo(
                self.archivo_seleccionado.nombre_archivo
            )

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_lista_archivos()
                self.archivo_seleccionado = None
            else:
                messagebox.showerror("Error", mensaje)

    def eliminar_permanente(self):
        if not self.modo_papelera:
            messagebox.showinfo("Modo Papelera", "Active el modo papelera primero")
            return

        if not self.archivo_seleccionado:
            messagebox.showwarning(
                "Sin selección", "Seleccione un archivo de la papelera"
            )
            return

        respuesta = messagebox.askyesno(
            "¡ADVERTENCIA!",
            f"¿Eliminar PERMANENTEMENTE '{self.archivo_seleccionado.nombre_archivo}'?\n\nEsta acción no se puede deshacer.",
        )

        if respuesta:
            exito, mensaje = self.gestor_archivos.eliminar_permanente(
                self.archivo_seleccionado.nombre_archivo
            )

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_lista_archivos()
                self.archivo_seleccionado = None
            else:
                messagebox.showerror("Error", mensaje)

    def cerrar_sesion(self):
        respuesta = messagebox.askyesno(
            "Cerrar Sesión",
            f"¿Desea cerrar la sesión de {self.usuario.nombre_usuario}?",
        )
        if respuesta:
            self.cerrar_sesion_activo = True
            self.ventana.destroy()

    def salir(self):
        respuesta = messagebox.askyesno("Salir", "¿Desea salir del sistema?")
        if respuesta:
            self.ventana.destroy()

    def mostrar(self):
        self.ventana.mainloop()
        return self.cerrar_sesion_activo
