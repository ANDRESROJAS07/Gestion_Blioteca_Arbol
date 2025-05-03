import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pickle
import os

# Clase Nodo para árboles binarios de búsqueda
class Nodo:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.izquierda = None
        self.derecha = None

# Clase Árbol Binario de Búsqueda
class ArbolBinario:
    def __init__(self):
        self.raiz = None
        self.tamano = 0
    
    def _insertar(self, clave, valor, nodo_actual):
        if clave < nodo_actual.clave:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = Nodo(clave, valor)
            else:
                self._insertar(clave, valor, nodo_actual.izquierda)
        elif clave > nodo_actual.clave:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = Nodo(clave, valor)
            else:
                self._insertar(clave, valor, nodo_actual.derecha)
        else:
            # La clave ya existe, actualizamos el valor
            nodo_actual.valor = valor
    
    def insertar(self, clave, valor):
        if self.raiz is None:
            self.raiz = Nodo(clave, valor)
            self.tamano += 1
        else:
            self._insertar(clave, valor, self.raiz)
            self.tamano += 1
    
    def _buscar(self, clave, nodo_actual):
        if not nodo_actual:
            return None
        if clave == nodo_actual.clave:
            return nodo_actual.valor
        elif clave < nodo_actual.clave:
            return self._buscar(clave, nodo_actual.izquierda)
        else:
            return self._buscar(clave, nodo_actual.derecha)
    
    def buscar(self, clave):
        if self.raiz is None:
            return None
        return self._buscar(clave, self.raiz)
    
    def _eliminar(self, clave, nodo_actual):
        if not nodo_actual:
            return None
        
        if clave < nodo_actual.clave:
            nodo_actual.izquierda = self._eliminar(clave, nodo_actual.izquierda)
        elif clave > nodo_actual.clave:
            nodo_actual.derecha = self._eliminar(clave, nodo_actual.derecha)
        else:
            # Nodo con solo un hijo o sin hijos
            if nodo_actual.izquierda is None:
                return nodo_actual.derecha
            elif nodo_actual.derecha is None:
                return nodo_actual.izquierda
            
            # Nodo con dos hijos
            # Encontramos el sucesor más pequeño en el subárbol derecho
            temp = self._encontrar_min(nodo_actual.derecha)
            nodo_actual.clave = temp.clave
            nodo_actual.valor = temp.valor
            
            # Eliminamos el sucesor más pequeño
            nodo_actual.derecha = self._eliminar(temp.clave, nodo_actual.derecha)
        
        return nodo_actual
    
    def _encontrar_min(self, nodo):
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual
    
    def eliminar(self, clave):
        if self.raiz:
            self.raiz = self._eliminar(clave, self.raiz)
            self.tamano -= 1
    
    def _inorden(self, nodo, lista):
        if nodo:
            self._inorden(nodo.izquierda, lista)
            lista.append((nodo.clave, nodo.valor))
            self._inorden(nodo.derecha, lista)
        return lista
    
    def listar_todos(self):
        return self._inorden(self.raiz, [])
    
    def __len__(self):
        return self.tamano


# Clases para la biblioteca
class Libro:
    def __init__(self, isbn, titulo, autor, categoria):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.disponible = True
        self.usuario_prestamo = None
        self.fecha_prestamo = None
    
    def __str__(self):
        estado = "Disponible" if self.disponible else f"Prestado a {self.usuario_prestamo}"
        return f"ISBN: {self.isbn}, Título: {self.titulo}, Autor: {self.autor}, Categoría: {self.categoria}, Estado: {estado}"


class Usuario:
    def __init__(self, id, nombre, apellido, email):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.libros_prestados = []
    
    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre} {self.apellido}, Email: {self.email}, Libros prestados: {len(self.libros_prestados)}"


class Biblioteca:
    def __init__(self):
        self.libros = ArbolBinario()
        self.usuarios = ArbolBinario()
        self.cargar_datos()
    
    def cargar_datos(self):
        try:
            if os.path.exists("libros.dat"):
                with open("libros.dat", "rb") as f:
                    libros_data = pickle.load(f)
                    for isbn, libro in libros_data:
                        self.libros.insertar(isbn, libro)
            
            if os.path.exists("usuarios.dat"):
                with open("usuarios.dat", "rb") as f:
                    usuarios_data = pickle.load(f)
                    for id, usuario in usuarios_data:
                        self.usuarios.insertar(id, usuario)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {e}")
    
    def guardar_datos(self):
        try:
            with open("libros.dat", "wb") as f:
                pickle.dump(self.libros.listar_todos(), f)
            
            with open("usuarios.dat", "wb") as f:
                pickle.dump(self.usuarios.listar_todos(), f)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar datos: {e}")
    
    def agregar_libro(self, isbn, titulo, autor, categoria):
        if self.libros.buscar(isbn):
            return False
        
        libro = Libro(isbn, titulo, autor, categoria)
        self.libros.insertar(isbn, libro)
        self.guardar_datos()
        return True
        
    def eliminar_libro(self, isbn):
        libro = self.buscar_libro(isbn)
        if not libro:
            return False, "No se encontró el libro con el ISBN especificado"
            
        if not libro.disponible:
            return False, "No se puede eliminar un libro que está prestado"
            
        self.libros.eliminar(isbn)
        self.guardar_datos()
        return True, "Libro eliminado correctamente"
    
    def agregar_usuario(self, id, nombre, apellido, email):
        if self.usuarios.buscar(id):
            return False
        
        usuario = Usuario(id, nombre, apellido, email)
        self.usuarios.insertar(id, usuario)
        self.guardar_datos()
        return True
    
    def buscar_libro(self, isbn):
        return self.libros.buscar(isbn)
    
    def buscar_usuario(self, id):
        return self.usuarios.buscar(id)
    
    def listar_libros(self):
        return self.libros.listar_todos()
    
    def listar_usuarios(self):
        return self.usuarios.listar_todos()
    
    def prestar_libro(self, isbn, id_usuario):
        libro = self.buscar_libro(isbn)
        usuario = self.buscar_usuario(id_usuario)
        
        if not libro or not usuario:
            return False, "Libro o usuario no encontrado"
        
        if not libro.disponible:
            return False, "El libro no está disponible"
        
        import datetime
        libro.disponible = False
        libro.usuario_prestamo = id_usuario
        libro.fecha_prestamo = datetime.datetime.now()
        usuario.libros_prestados.append(isbn)
        
        self.guardar_datos()
        return True, "Préstamo realizado con éxito"
    
    def devolver_libro(self, isbn):
        libro = self.buscar_libro(isbn)
        
        if not libro:
            return False, "Libro no encontrado"
        
        if libro.disponible:
            return False, "El libro ya está disponible"
        
        usuario = self.buscar_usuario(libro.usuario_prestamo)
        if usuario and isbn in usuario.libros_prestados:
            usuario.libros_prestados.remove(isbn)
        
        libro.disponible = True
        libro.usuario_prestamo = None
        libro.fecha_prestamo = None
        
        self.guardar_datos()
        return True, "Devolución realizada con éxito"
    
    def libros_prestados_usuario(self, id_usuario):
        usuario = self.buscar_usuario(id_usuario)
        if not usuario:
            return []
        
        libros_prestados = []
        for isbn in usuario.libros_prestados:
            libro = self.buscar_libro(isbn)
            if libro:
                libros_prestados.append(libro)
        
        return libros_prestados


# Interfaz gráfica
class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Biblioteca")
        self.root.geometry("900x600")
        self.biblioteca = Biblioteca()
        
        self._crear_widgets()
    
    def _crear_widgets(self):
        # Crear pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña Libros
        self.tab_libros = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_libros, text="Libros")
        
        # Pestaña Usuarios
        self.tab_usuarios = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_usuarios, text="Usuarios")
        
        # Pestaña Préstamos
        self.tab_prestamos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_prestamos, text="Préstamos")
        
        # Configurar pestañas
        self._configurar_tab_libros()
        self._configurar_tab_usuarios()
        self._configurar_tab_prestamos()
    
    def _configurar_tab_libros(self):
        # Frame para agregar libros
        frame_agregar = ttk.LabelFrame(self.tab_libros, text="Agregar Libro")
        frame_agregar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_agregar, text="ISBN:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.isbn_entry = ttk.Entry(frame_agregar, width=20)
        self.isbn_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(frame_agregar, text="Título:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.titulo_entry = ttk.Entry(frame_agregar, width=30)
        self.titulo_entry.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(frame_agregar, text="Autor:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.autor_entry = ttk.Entry(frame_agregar, width=20)
        self.autor_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(frame_agregar, text="Categoría:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.categoria_entry = ttk.Entry(frame_agregar, width=20)
        self.categoria_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
        
        btn_agregar = ttk.Button(frame_agregar, text="Agregar Libro", command=self.agregar_libro)
        btn_agregar.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        btn_eliminar = ttk.Button(frame_agregar, text="Eliminar Libro", command=self.eliminar_libro)
        btn_eliminar.grid(row=2, column=2, columnspan=2, padx=5, pady=5)
        
        # Frame para buscar libros
        frame_buscar = ttk.LabelFrame(self.tab_libros, text="Buscar Libro")
        frame_buscar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_buscar, text="ISBN:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.buscar_isbn_entry = ttk.Entry(frame_buscar, width=20)
        self.buscar_isbn_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        btn_buscar = ttk.Button(frame_buscar, text="Buscar", command=self.buscar_libro)
        btn_buscar.grid(row=0, column=2, padx=5, pady=5)
        
        # Tabla de libros
        frame_tabla = ttk.LabelFrame(self.tab_libros, text="Listado de Libros")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Frame para botones de acción
        frame_acciones = ttk.Frame(frame_tabla)
        frame_acciones.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)
        
        btn_eliminar_seleccionado = ttk.Button(frame_acciones, text="Eliminar Seleccionado", 
                                             command=self.eliminar_libro_seleccionado)
        btn_eliminar_seleccionado.pack(side=tk.LEFT, padx=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tabla_libros = ttk.Treeview(frame_tabla, columns=("isbn", "titulo", "autor", "categoria", "estado"), 
                                        show="headings", yscrollcommand=scrollbar.set)
        self.tabla_libros.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tabla_libros.yview)
        
        # Configurar columnas
        self.tabla_libros.heading("isbn", text="ISBN")
        self.tabla_libros.heading("titulo", text="Título")
        self.tabla_libros.heading("autor", text="Autor")
        self.tabla_libros.heading("categoria", text="Categoría")
        self.tabla_libros.heading("estado", text="Estado")
        
        self.tabla_libros.column("isbn", width=100)
        self.tabla_libros.column("titulo", width=200)
        self.tabla_libros.column("autor", width=150)
        self.tabla_libros.column("categoria", width=100)
        self.tabla_libros.column("estado", width=150)
        
        # Botón para refrescar
        btn_refrescar = ttk.Button(self.tab_libros, text="Refrescar Lista", command=self.actualizar_libros)
        btn_refrescar.pack(pady=5)
        
        # Inicializar tabla
        self.actualizar_libros()
    
    def _configurar_tab_usuarios(self):
        # Frame para agregar usuarios
        frame_agregar = ttk.LabelFrame(self.tab_usuarios, text="Agregar Usuario")
        frame_agregar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_agregar, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.id_entry = ttk.Entry(frame_agregar, width=20)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(frame_agregar, text="Nombre:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.nombre_entry = ttk.Entry(frame_agregar, width=20)
        self.nombre_entry.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(frame_agregar, text="Apellido:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.apellido_entry = ttk.Entry(frame_agregar, width=20)
        self.apellido_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(frame_agregar, text="Email:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.email_entry = ttk.Entry(frame_agregar, width=20)
        self.email_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
        
        btn_agregar = ttk.Button(frame_agregar, text="Agregar Usuario", command=self.agregar_usuario)
        btn_agregar.grid(row=2, column=0, columnspan=4, padx=5, pady=5)
        
        # Frame para buscar usuarios
        frame_buscar = ttk.LabelFrame(self.tab_usuarios, text="Buscar Usuario")
        frame_buscar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_buscar, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.buscar_id_entry = ttk.Entry(frame_buscar, width=20)
        self.buscar_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        btn_buscar = ttk.Button(frame_buscar, text="Buscar", command=self.buscar_usuario)
        btn_buscar.grid(row=0, column=2, padx=5, pady=5)
        
        btn_ver_libros = ttk.Button(frame_buscar, text="Ver Libros Prestados", command=self.ver_libros_prestados)
        btn_ver_libros.grid(row=0, column=3, padx=5, pady=5)
        
        # Tabla de usuarios
        frame_tabla = ttk.LabelFrame(self.tab_usuarios, text="Listado de Usuarios")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tabla_usuarios = ttk.Treeview(frame_tabla, columns=("id", "nombre", "apellido", "email", "libros"), 
                                          show="headings", yscrollcommand=scrollbar.set)
        self.tabla_usuarios.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tabla_usuarios.yview)
        
        # Configurar columnas
        self.tabla_usuarios.heading("id", text="ID")
        self.tabla_usuarios.heading("nombre", text="Nombre")
        self.tabla_usuarios.heading("apellido", text="Apellido")
        self.tabla_usuarios.heading("email", text="Email")
        self.tabla_usuarios.heading("libros", text="Libros prestados")
        
        self.tabla_usuarios.column("id", width=100)
        self.tabla_usuarios.column("nombre", width=150)
        self.tabla_usuarios.column("apellido", width=150)
        self.tabla_usuarios.column("email", width=200)
        self.tabla_usuarios.column("libros", width=100)
        
        # Botón para refrescar
        btn_refrescar = ttk.Button(self.tab_usuarios, text="Refrescar Lista", command=self.actualizar_usuarios)
        btn_refrescar.pack(pady=5)
        
        # Inicializar tabla
        self.actualizar_usuarios()
    
    def _configurar_tab_prestamos(self):
        # Frame para préstamos
        frame_prestamo = ttk.LabelFrame(self.tab_prestamos, text="Realizar Préstamo")
        frame_prestamo.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_prestamo, text="ISBN del Libro:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.prestamo_isbn_entry = ttk.Entry(frame_prestamo, width=20)
        self.prestamo_isbn_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(frame_prestamo, text="ID del Usuario:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.prestamo_id_entry = ttk.Entry(frame_prestamo, width=20)
        self.prestamo_id_entry.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        btn_prestar = ttk.Button(frame_prestamo, text="Realizar Préstamo", command=self.prestar_libro)
        btn_prestar.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
        
        # Frame para devoluciones
        frame_devolucion = ttk.LabelFrame(self.tab_prestamos, text="Realizar Devolución")
        frame_devolucion.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_devolucion, text="ISBN del Libro:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.devolucion_isbn_entry = ttk.Entry(frame_devolucion, width=20)
        self.devolucion_isbn_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        btn_devolver = ttk.Button(frame_devolucion, text="Realizar Devolución", command=self.devolver_libro)
        btn_devolver.grid(row=0, column=2, columnspan=2, padx=5, pady=5)
        
        # Tabla de libros prestados
        frame_tabla = ttk.LabelFrame(self.tab_prestamos, text="Libros Prestados")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tabla_prestamos = ttk.Treeview(frame_tabla, 
                                           columns=("isbn", "titulo", "usuario", "fecha"), 
                                           show="headings", 
                                           yscrollcommand=scrollbar.set)
        self.tabla_prestamos.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tabla_prestamos.yview)
        
        # Configurar columnas
        self.tabla_prestamos.heading("isbn", text="ISBN")
        self.tabla_prestamos.heading("titulo", text="Título")
        self.tabla_prestamos.heading("usuario", text="Usuario")
        self.tabla_prestamos.heading("fecha", text="Fecha Préstamo")
        
        self.tabla_prestamos.column("isbn", width=100)
        self.tabla_prestamos.column("titulo", width=200)
        self.tabla_prestamos.column("usuario", width=150)
        self.tabla_prestamos.column("fecha", width=150)
        
        # Botón para refrescar
        btn_refrescar = ttk.Button(self.tab_prestamos, text="Refrescar Lista", command=self.actualizar_prestamos)
        btn_refrescar.pack(pady=5)
        
        # Inicializar tabla
        self.actualizar_prestamos()
    
    def agregar_libro(self):
        isbn = self.isbn_entry.get().strip()
        titulo = self.titulo_entry.get().strip()
        autor = self.autor_entry.get().strip()
        categoria = self.categoria_entry.get().strip()
        
        if not isbn or not titulo or not autor or not categoria:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        if self.biblioteca.agregar_libro(isbn, titulo, autor, categoria):
            messagebox.showinfo("Éxito", f"Libro '{titulo}' agregado correctamente")
            self.actualizar_libros()
            
            # Limpiar campos
            self.isbn_entry.delete(0, tk.END)
            self.titulo_entry.delete(0, tk.END)
            self.autor_entry.delete(0, tk.END)
            self.categoria_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"El libro con ISBN {isbn} ya existe")
    
    def agregar_usuario(self):
        id = self.id_entry.get().strip()
        nombre = self.nombre_entry.get().strip()
        apellido = self.apellido_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not id or not nombre or not apellido or not email:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        if self.biblioteca.agregar_usuario(id, nombre, apellido, email):
            messagebox.showinfo("Éxito", f"Usuario '{nombre} {apellido}' agregado correctamente")
            self.actualizar_usuarios()
            
            # Limpiar campos
            self.id_entry.delete(0, tk.END)
            self.nombre_entry.delete(0, tk.END)
            self.apellido_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"El usuario con ID {id} ya existe")
    
    def buscar_libro(self):
        isbn = self.buscar_isbn_entry.get().strip()
        
        if not isbn:
            messagebox.showerror("Error", "Ingrese un ISBN para buscar")
            return
        
        libro = self.biblioteca.buscar_libro(isbn)
        if libro:
            messagebox.showinfo("Libro encontrado", str(libro))
        else:
            messagebox.showerror("Error", f"No se encontró un libro con ISBN {isbn}")
    
    def buscar_usuario(self):
        id = self.buscar_id_entry.get().strip()
        
        if not id:
            messagebox.showerror("Error", "Ingrese un ID para buscar")
            return
        
        usuario = self.biblioteca.buscar_usuario(id)
        if usuario:
            messagebox.showinfo("Usuario encontrado", str(usuario))
        else:
            messagebox.showerror("Error", f"No se encontró un usuario con ID {id}")
    
    def ver_libros_prestados(self):
        id = self.buscar_id_entry.get().strip()
        
        if not id:
            messagebox.showerror("Error", "Ingrese un ID de usuario")
            return
        
        usuario = self.biblioteca.buscar_usuario(id)
        if not usuario:
            messagebox.showerror("Error", f"No se encontró un usuario con ID {id}")
            return
        
        libros_prestados = self.biblioteca.libros_prestados_usuario(id)
        
        if not libros_prestados:
            messagebox.showinfo("Información", f"El usuario {usuario.nombre} {usuario.apellido} no tiene libros prestados")
            return
        
        # Mostrar ventana con libros prestados
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Libros prestados a {usuario.nombre} {usuario.apellido}")
        ventana.geometry("700x300")
        
        # Tabla
        frame = ttk.Frame(ventana)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        tabla = ttk.Treeview(frame, columns=("isbn", "titulo", "autor", "fecha"), 
                             show="headings", yscrollcommand=scrollbar.set)
        tabla.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=tabla.yview)
        
        # Configurar columnas
        tabla.heading("isbn", text="ISBN")
        tabla.heading("titulo", text="Título")
        tabla.heading("autor", text="Autor")
        tabla.heading("fecha", text="Fecha Préstamo")
        
        tabla.column("isbn", width=100)
        tabla.column("titulo", width=200)
        tabla.column("autor", width=150)
        tabla.column("fecha", width=150)
        
        # Llenar tabla
        for libro in libros_prestados:
            fecha = libro.fecha_prestamo.strftime("%d/%m/%Y %H:%M") if libro.fecha_prestamo else ""
            tabla.insert("", tk.END, values=(libro.isbn, libro.titulo, libro.autor, fecha))
    
    def prestar_libro(self):
        isbn = self.prestamo_isbn_entry.get().strip()
        id_usuario = self.prestamo_id_entry.get().strip()
        
        if not isbn or not id_usuario:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        resultado, mensaje = self.biblioteca.prestar_libro(isbn, id_usuario)
        
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.actualizar_prestamos()
            self.actualizar_libros()
            self.actualizar_usuarios()
            
            # Limpiar campos
            self.prestamo_isbn_entry.delete(0, tk.END)
            self.prestamo_id_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", mensaje)
    
    def devolver_libro(self):
        isbn = self.devolucion_isbn_entry.get().strip()
        
        if not isbn:
            messagebox.showerror("Error", "Ingrese un ISBN para devolver")
            return
        
        resultado, mensaje = self.biblioteca.devolver_libro(isbn)
        
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.actualizar_prestamos()
            self.actualizar_libros()
            self.actualizar_usuarios()
            
            # Limpiar campos
            self.devolucion_isbn_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", mensaje)
    
    def actualizar_libros(self):
        # Limpiar tabla
        for item in self.tabla_libros.get_children():
            self.tabla_libros.delete(item)
        
        # Obtener todos los libros
        libros = self.biblioteca.listar_libros()
        
        # Llenar tabla
        for _, libro in libros:
            estado = "Disponible" if libro.disponible else f"Prestado a {libro.usuario_prestamo}"
            self.tabla_libros.insert("", tk.END, values=(libro.isbn, libro.titulo, libro.autor, libro.categoria, estado))
    
    def actualizar_usuarios(self):
        # Limpiar tabla
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)
        
        # Obtener todos los usuarios
        usuarios = self.biblioteca.listar_usuarios()
        
        # Llenar tabla
        for _, usuario in usuarios:
            self.tabla_usuarios.insert("", tk.END, values=(usuario.id, usuario.nombre, usuario.apellido, usuario.email, len(usuario.libros_prestados)))
    
    def actualizar_prestamos(self):
        # Limpiar tabla
        for item in self.tabla_prestamos.get_children():
            self.tabla_prestamos.delete(item)
        
        # Obtener todos los libros prestados
        libros = self.biblioteca.listar_libros()
        libros_prestados = [(_, libro) for _, libro in libros if not libro.disponible]
        
        # Llenar tabla
        for _, libro in libros_prestados:
            usuario = self.biblioteca.buscar_usuario(libro.usuario_prestamo)
            nombre_usuario = f"{usuario.nombre} {usuario.apellido}" if usuario else libro.usuario_prestamo
            fecha = libro.fecha_prestamo.strftime("%d/%m/%Y %H:%M") if libro.fecha_prestamo else ""
            self.tabla_prestamos.insert("", tk.END, values=(libro.isbn, libro.titulo, nombre_usuario, fecha))
            
    def eliminar_libro(self):
        isbn = self.isbn_entry.get().strip()
        
        if not isbn:
            messagebox.showerror("Error", "Ingrese el ISBN del libro a eliminar")
            return
            
        resultado, mensaje = self.biblioteca.eliminar_libro(isbn)
        
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.actualizar_libros()
            
            # Limpiar campos
            self.isbn_entry.delete(0, tk.END)
            self.titulo_entry.delete(0, tk.END)
            self.autor_entry.delete(0, tk.END)
            self.categoria_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", mensaje)
    
    def eliminar_libro_seleccionado(self):
        seleccion = self.tabla_libros.selection()
        
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un libro de la lista")
            return
            
        item = self.tabla_libros.item(seleccion[0])
        isbn = item['values'][0]
        titulo = item['values'][1]
        
        # Confirmar eliminación
        confirmacion = messagebox.askyesno("Confirmar eliminación", 
                                        f"¿Está seguro de eliminar el libro '{titulo}' con ISBN {isbn}?")
        
        if confirmacion:
            resultado, mensaje = self.biblioteca.eliminar_libro(isbn)
            
            if resultado:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_libros()
            else:
                messagebox.showerror("Error", mensaje)

# Función principal
def main():
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()