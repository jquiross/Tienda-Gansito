import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk 
import pymongo
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import defaultdict
from tkinter import Menu


mongo_uri="mongodb+srv://fernando:1234@cluster0.cbzibdn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
my_client = pymongo.MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True)


#Boton Usuarios 
def button_click_usuarios(id_usuario,nombre_usuarios,apellido1_usuarios,apellido2_usuarios,email_usuarios,rol_usuarios): 
     
    if id_usuario > 0:
        ventana_editar_usuario(id_usuario,nombre_usuarios,apellido1_usuarios,apellido2_usuarios,email_usuarios,rol_usuarios)
    else:
        messagebox.showerror("Error", f"No se pudo encontrar el producto con id {id_usuario}.")

#Boton Roles
def button_click_roles(row_id): #ESTO ES UNA PRUEBA, REEMPLAZAR POR VALOR CORRECTO
    
    print("Button clicked for row:", row_id)

#Boton Proveedor
def button_click_proveedor(id_proveedor, proveedor_descripcion):  
     
  if id_proveedor > 0:
        ventana_editar_proveedor(id_proveedor,proveedor_descripcion)
  else:
        messagebox.showerror("Error", f"No se pudo encontrar el proveedor con id {id_proveedor}.")

#Boton Categorias
def button_click_categorias(id_categoria, categoria_descripcion):  
      
  if id_categoria > 0:
        ventana_editar_categoria(id_categoria,categoria_descripcion)
  else:
        messagebox.showerror("Error", f"No se pudo encontrar la categoria con id {id_categoria}.")

#Boton Almacen
def button_click_almacen(id_almacen, nombre_almacen, nombre_producto,localizacion,cantidad):  

   if id_almacen > 0:
        ventana_editar_almacen(id_almacen, nombre_almacen, nombre_producto,localizacion,cantidad)
   else:
        messagebox.showerror("Error", f"No se pudo encontrar el almacen con id {id_almacen}.")

#Boton Reportes
def button_click_reportes(id_reporte,fecha,id_producto): #ESTO ES UNA PRUEBA, REEMPLAZAR POR VALOR CORRECTO
     if id_reporte > 0:
        ventana_editar_reporte(id_reporte,fecha,id_producto)
     else:
        messagebox.showerror("Error", f"No se pudo encontrar el producto con id {id_reporte}.")
    

#Boton Productos
def button_click_productos(id_producto,nombre_producto,descripcion_producto,precio_producto,proovedor_producto,categorias_producto,fechaIngreso_producto):
    
    if id_producto > 0:
        ventana_editar_producto(id_producto,nombre_producto,descripcion_producto,precio_producto,proovedor_producto,categorias_producto,fechaIngreso_producto)
    else:
        messagebox.showerror("Error", f"No se pudo encontrar el producto con id {id_producto}.")


# Funciones para manejar las diferentes opciones del menú Ver

def manejar_opcion_ver_usuarios():

    ventana_usua = tk.Toplevel()
    ventana_usua.title("Lista de Usuarios")
    ventana_usua.geometry("1000x600+300+200")
    ventana_usua.resizable(True, True)
    
    tablaUsuario = ttk.Treeview(ventana_usua, columns=("Editar", "id_usuario","Nombre", "Apellido 1", "Apellido 2", "Email","Rol"))
    tablaUsuario.heading("Editar", text="Opcion")
    tablaUsuario.heading("id_usuario", text="Id  ")
    tablaUsuario.heading("Nombre", text="Nombre")
    tablaUsuario.heading("Apellido 1", text="1er Apellido")
    tablaUsuario.heading("Apellido 2", text="2do Apellido")
    tablaUsuario.heading("Email", text="Email")
    tablaUsuario.heading("Rol", text="Rol  ")

    tablaUsuario.column("#0", stretch=tk.NO, width=20)
    tablaUsuario.column("Editar", width=60)
    tablaUsuario.column("id_usuario", stretch=tk.NO, width=50)
    tablaUsuario.column("Nombre", width=90)
    tablaUsuario.column("Apellido 1", width=90)
    tablaUsuario.column("Apellido 2", width=90)
    tablaUsuario.column("Email", width=120)
    tablaUsuario.column("Rol", width=120 )

    my_database = my_client.Inventario
    my_collection = my_database['Usuario']
    roles_collection =  my_database['Roles']

    pipeline = [
     {
        '$lookup': {
            'from': 'Roles',
            'localField': 'id_rol',
            'foreignField': 'id_rol',
            'as': 'rol_info'
        }
    },
    {
        '$unwind': '$rol_info'
    },
    {
        '$project': {
            
            "id_usuario":1,   
            "nombre": 1,
            "apellido1": 1,
            "apellido2": 1,
            "email": 1,
            "rol_descripcion": '$rol_info.rol_descripcion',
            "_id": 0 
            
        }
    }
    ]

    result_cursor = my_collection.aggregate(pipeline)
    lista = list(result_cursor)

    #On Select Linea Usuarios
    def on_select_usuarios(event):
    
     item = tablaUsuario.focus()
     if item:
        id_usuario = tablaUsuario.item(item)['values'][1]
        nombre = tablaUsuario.item(item)['values'][2]
        apellido1 = tablaUsuario.item(item)['values'][3]
        apellido2 = tablaUsuario.item(item)['values'][4]
        email = tablaUsuario.item(item)['values'][5]
        query =  roles_collection.find_one({'rol_descripcion': tablaUsuario.item(item)['values'][6]}, {"_id": 0, "id_rol": 1})   
        id_rol = query["id_rol"]
        ventana_usua.destroy()
        button_click_usuarios( id_usuario,nombre,apellido1,apellido2,email,id_rol)
    
    for item in lista:
      print(item)       
      tablaUsuario.insert('', 'end', values=('Editar', item["id_usuario"], item["nombre"], 
                                               item["apellido1"],item["apellido2"], item["email"], 
                                               item["rol_descripcion"]))

    tablaUsuario.bind('<<TreeviewSelect>>', on_select_usuarios)

    tablaUsuario.pack(expand=True, fill="both")

def manejar_opcion_ver_roles():
    
    ventana_rol = tk.Toplevel()
    ventana_rol.title("Lista de Roles")
    ventana_rol.geometry("200x150+600+200")
    ventana_rol.resizable(True, True)

    tablaRoles = ttk.Treeview(ventana_rol, columns=("id_rol","rol_descripcion"))
    tablaRoles.heading("id_rol", text="ID")
    tablaRoles.heading("rol_descripcion", text="Descripcion")
 
    tablaRoles.column("#0", stretch=tk.NO, width=20)
    tablaRoles.column("id_rol", stretch=tk.NO, width=30)
    tablaRoles.column("rol_descripcion", width=30)

    my_database = my_client.Inventario
    my_collection = my_database.Roles

    campos = {
    "id_rol": 1,
    "rol_descripcion": 1,
    "_id": 0 
     }

    my_cursor = my_collection.find({}, campos)

    lista = []

    for item in my_cursor:
     lista.append(item)

    def on_select_roles(event):
    
     item = tablaRoles.focus()
     if item:
        button_click_roles(tablaRoles.item(item)['values'])

    for item in lista:
     row_id = tablaRoles.insert('', 'end', values=( item["id_rol"], item["rol_descripcion"]))
 
    tablaRoles.bind('<<TreeviewSelect>>', on_select_roles)

    tablaRoles.pack(expand=True, fill="both")

def manejar_opcion_ver_proveedores():
    ventana_prov = tk.Toplevel()
    ventana_prov.title("Lista de Proveedores")
    ventana_prov.geometry("500x300+600+200")
    ventana_prov.resizable(True, True)

    tablaProveedor = ttk.Treeview(ventana_prov, columns=("Editar","id_proveedor","proveedor_descripcion"))
    tablaProveedor.heading("Editar", text="Opcion")
    tablaProveedor.heading("id_proveedor", text="ID")
    tablaProveedor.heading("proveedor_descripcion", text="Descripcion del Proveedor")
 
    tablaProveedor.column("#0", stretch=tk.NO, width=20)
    tablaProveedor.column("Editar", width=30)
    tablaProveedor.column("id_proveedor", stretch=tk.NO, width=30)
    tablaProveedor.column("proveedor_descripcion", width=50)

    my_database = my_client.Inventario
    my_collection = my_database.Proveedor

    campos = {
    "id_proveedor": 1,
    "proveedor_descripcion": 1,
    "_id": 0 
     }

    my_cursor = my_collection.find({}, campos)

    lista = []

    for item in my_cursor:
     lista.append(item)

    def on_select_proveedor(event):
    
     item = tablaProveedor.focus()
     if item:

        id_proveedor = tablaProveedor.item(item)['values'][1]
        proveedor_descripcion = tablaProveedor.item(item)['values'][2]

        ventana_prov.destroy() #Cerrar la ventana antes de editar
        button_click_proveedor(id_proveedor,proveedor_descripcion)

    for item in lista:
     row_id = tablaProveedor.insert('', 'end', values=( "Editar",item["id_proveedor"], item["proveedor_descripcion"]))
 
    tablaProveedor.bind('<<TreeviewSelect>>', on_select_proveedor)

    tablaProveedor.pack(expand=True, fill="both")
 
def manejar_opcion_ver_almacen():
    
    ventana_alma = tk.Toplevel()
    ventana_alma.title("Inventario de Almacenes")
    ventana_alma.geometry("1000x500+400+200")
    ventana_alma.resizable(True, True)
 
    my_database = my_client.Inventario
    mycollection = my_database['Almacen']
   
    #Agregacion de campos (simula un join)
    pipeline = [
     {
        '$lookup': {
            'from': 'Productos',
            'localField': 'id_producto',
            'foreignField': 'id_producto',
            'as': 'producto_info'
        }
    },
    {
        '$unwind': '$producto_info'
    },
    {
        '$project': {
            'id_almacen': 1,
            'id_producto': 1,
            'nombre_producto':'$producto_info.nombre_producto',
            'nombre_almacen': 1,
            'localizacion': 1,
            'cantidad': 1
        }
    }
    ]
    result_cursor = mycollection.aggregate(pipeline)
    results_list = list(result_cursor)

    tablaAlmacen = ttk.Treeview(ventana_alma, columns=("Editar","id_almacen","id_producto","nombre_producto", "nombre_almacen", 
                                                              "localizacion","cantidad"))
    tablaAlmacen.heading("Editar", text="Opcion")
    tablaAlmacen.heading("id_almacen", text="ID Almacen")
    tablaAlmacen.heading("id_producto", text="ID Producto")
    tablaAlmacen.heading("nombre_producto", text="Producto")
    tablaAlmacen.heading("nombre_almacen", text="Nombre de Almacen")
    tablaAlmacen.heading("localizacion", text="Localizacion")
    tablaAlmacen.heading("cantidad", text="Cantidad Disponible")

    tablaAlmacen.column("#0", stretch=tk.NO, width=20)
    tablaAlmacen.column("Editar", stretch=tk.NO, width=70)
    tablaAlmacen.column("id_almacen", stretch=tk.NO, width=70)
    tablaAlmacen.column("id_producto", stretch=tk.NO, width=70)
    tablaAlmacen.column("nombre_producto", width=70)
    tablaAlmacen.column("nombre_almacen", width=70)
    tablaAlmacen.column("localizacion", width=70)
    tablaAlmacen.column("cantidad", width=30)

  
    for item in results_list:
      print(item)       
      tablaAlmacen.insert('', 'end', values=('Editar', item["id_almacen"], item["id_producto"], 
                                               item["nombre_producto"],item["nombre_almacen"], item["localizacion"], 
                                               item["cantidad"]))
  #ONSELECU
    def on_select_almacen(event):
    
     item = tablaAlmacen.focus()
     if item:
         
         id_almacen = tablaAlmacen.item(item)['values'][1]
         nombre_almacen = tablaAlmacen.item(item)['values'][4]
         nombre_producto = tablaAlmacen.item(item)['values'][3]
         localizacion = tablaAlmacen.item(item)['values'][5]
         cantidad = tablaAlmacen.item(item)['values'][6]
     
     ventana_alma.destroy() #Cerrar la ventana antes de editar
     button_click_almacen(id_almacen, nombre_almacen, nombre_producto,localizacion,cantidad)

    tablaAlmacen.bind('<<TreeviewSelect>>', on_select_almacen)

    tablaAlmacen.pack(expand=True, fill="both")

def manejar_opcion_ver_reportes():
    ventana_rep = tk.Toplevel()
    ventana_rep.title("Lista de Reportes")
    ventana_rep.geometry("500x400+600+200")
    ventana_rep.resizable(True, True)

    tablaReportes = ttk.Treeview(ventana_rep, columns=("Editar","id_reporte","fecha","id_producto"))
    tablaReportes.heading("Editar", text="Opcion")
    tablaReportes.heading("id_reporte", text="Reporte")
    tablaReportes.heading("fecha", text="Fecha")
    tablaReportes.heading("id_producto", text="ID Producto")

    tablaReportes.column("#0", stretch=tk.NO, width=20)
    tablaReportes.column("Editar", width=30)
    tablaReportes.column("id_reporte", width=30)
    tablaReportes.column("fecha", width=80)
    tablaReportes.column("id_producto", width=30)
 
    my_database = my_client.Inventario
    my_collection = my_database.Reportes

    campos = {
        "id_reporte": 1,
        "fecha": 1,
        "id_producto": 1,
        "_id": 0 
    }

    my_cursor = my_collection.find({}, campos)

    lista = []

    for item in my_cursor:
        lista.append(item)

    def on_select_reportes(event):
        item = tablaReportes.focus()
        if item:
            id_reporte = tablaReportes.item(item)['values'][1]
            fecha = tablaReportes.item(item)['values'][2]
            id_producto = tablaReportes.item(item)['values'][3]

            ventana_rep.destroy() 
            button_click_reportes(id_reporte, fecha , id_producto )

    for item in lista:
        row_id = tablaReportes.insert('', 'end', values=("Editar", item["id_reporte"], item["fecha"], item["id_producto"]))
 
    tablaReportes.bind('<<TreeviewSelect>>', on_select_reportes)

    tablaReportes.pack(expand=True, fill="both")

def manejar_opcion_ver_categorias():
    ventana_cat = tk.Toplevel()
    ventana_cat.title("Ver Categoria")
    ventana_cat.geometry("400x400+600+200")
    ventana_cat.resizable(True, True)
    
    tablaCat = ttk.Treeview(ventana_cat, columns=("Editar","id_categoria","categoria_descripcion"))
    tablaCat.heading("Editar", text="Opcion")
    tablaCat.heading("id_categoria", text="ID")
    tablaCat.heading("categoria_descripcion", text="Descripcion")
 
    tablaCat.column("#0", stretch=tk.NO, width=20)
    tablaCat.column("Editar", width=30)
    tablaCat.column("id_categoria", stretch=tk.NO, width=30)
    tablaCat.column("categoria_descripcion", width=50)
    
    my_database = my_client.Inventario
    my_collection = my_database.Categorias

    campos = {
    "id_categoria": 1,
    "categoria_descripcion": 1,
    "_id": 0 
     }

    my_cursor = my_collection.find({}, campos)

    lista = []

    for item in my_cursor:
     lista.append(item)



    for item in lista:
     row_id = tablaCat.insert('', 'end', values=( "Editar",item["id_categoria"], item["categoria_descripcion"]))

    def on_select_cat(event):
    
     item = tablaCat.focus()
      
     if item:
        id_categoria = tablaCat.item(item)['values'][1]
        categoria_descripcion = tablaCat.item(item)['values'][2]

        ventana_cat.destroy() #Cerrar la ventana antes de editar
        button_click_categorias(id_categoria,categoria_descripcion)

    tablaCat.bind('<<TreeviewSelect>>', on_select_cat)

    tablaCat.pack(expand=True, fill="both")

def manejar_opcion_ver_productos():
     
    ventana_prod = tk.Toplevel()
    ventana_prod.title("Lista de Productos")
    ventana_prod.geometry("1000x600+300+200")
    ventana_prod.resizable(True, True)

    tablaProductos = ttk.Treeview(ventana_prod, columns=("Editar","id_producto","nombre_producto", "id_descripcion", 
                                                              "precio","id_proveedor", "categoria_descripcion", "fecha_ingreso"))
    tablaProductos.heading("Editar", text="Opcion")
    tablaProductos.heading("id_producto", text="ID")
    tablaProductos.heading("nombre_producto", text="Producto")
    tablaProductos.heading("id_descripcion", text="Descripcion")
    tablaProductos.heading("precio", text="Precio")
    tablaProductos.heading("id_proveedor", text="Proveedor")
    tablaProductos.heading("categoria_descripcion", text="Categoria")
    tablaProductos.heading("fecha_ingreso", text="Fecha de Ingreso")

    tablaProductos.column("#0", stretch=tk.NO, width=20)
    tablaProductos.column("Editar", stretch=tk.NO, width=40)
    tablaProductos.column("id_producto", stretch=tk.NO, width=20)
    tablaProductos.column("nombre_producto", width=110)
    tablaProductos.column("id_descripcion", width=150)
    tablaProductos.column("precio", width=20)
    tablaProductos.column("id_proveedor", width=90)
    tablaProductos.column("categoria_descripcion", width=90)
    tablaProductos.column("fecha_ingreso", width=90)

    my_database = my_client.Inventario
    mycollection = my_database['Productos']
   
    #Agregacion de campos (simula un join)
    pipeline = [
     {
        '$lookup': {
            'from': 'Categorias',
            'localField': 'id_categoria',
            'foreignField': 'id_categoria',
            'as': 'categoria_info'
        }
    },
    {
        '$unwind': '$categoria_info'
    },
   {
        '$lookup': {
            'from': 'Proveedor',
            'localField': 'id_proveedor',
            'foreignField': 'id_proveedor',
            'as': 'proveedor_info'
        }
    },
    {
        '$unwind': '$proveedor_info'
    },
       {
        '$lookup': {
            'from': 'Descripcion',
            'localField': 'id_descripcion',
            'foreignField': 'id_descripcion',
            'as': 'descripcion_info'
        }
    },
    {
        '$unwind': '$descripcion_info'
    },
           {
        '$lookup': {
            'from': 'Descripcion',
            'localField': 'id_descripcion',
            'foreignField': 'id_descripcion',
            'as': 'precio_info'
        }
    },
    {
        '$unwind': '$precio_info'
    },
    {
        '$project': {
            'id_producto': 1,
            'nombre_producto':1,
            'id_proveedor': '$proveedor_info.proveedor_descripcion',
            'precio': '$precio_info.precio',
            'id_descripcion': '$descripcion_info.producto_descripcion',
            'fecha_ingreso': 1,
            'categoria_descripcion':'$categoria_info.categoria_descripcion',
        }
    }
    ]
    result_cursor = mycollection.aggregate(pipeline)
    results_list = list(result_cursor)

    for item in results_list:
      print(item)       
      tablaProductos.insert('', 'end', values=('Editar', item["id_producto"], item["nombre_producto"], 
                                               item["id_descripcion"],item["precio"], item["id_proveedor"], 
                                               item["categoria_descripcion"], item["fecha_ingreso"]))
 
    def on_select_productos(event):
     item = tablaProductos.focus()
     if item:
        id_producto = tablaProductos.item(item)['values'][1]
        nombre_producto = tablaProductos.item(item)['values'][2]
        descripcion_producto= tablaProductos.item(item)['values'][3]
        precio_producto=tablaProductos.item(item)['values'][4]
        proovedor_producto=tablaProductos.item(item)['values'][5]
        categorias_producto=tablaProductos.item(item)['values'][6]
        fechaIngreso_producto=tablaProductos.item(item)['values'][7]

        ventana_prod.destroy() #Cerrar la ventana antes de editar
        button_click_productos(id_producto,nombre_producto,descripcion_producto,precio_producto,proovedor_producto,categorias_producto,fechaIngreso_producto)

    tablaProductos.bind('<<TreeviewSelect>>', on_select_productos)

    tablaProductos.pack(expand=True, fill="both")

#VENTANAS DE GRAFICOS

# Funciones para CREAR VENTANA Y GRAFICO CATEGORIAS
def crear_graficoCategorias(master):
    my_database = my_client.Inventario
    Productoscollection = my_database['Productos']
    Categoriascollection = my_database['Categorias']
    # Se utilizar para obtener la cantidad de productos en cada categoría
    categorias_productos = {}
    for producto in Productoscollection.find():
        categoria_id = producto['id_categoria']
        categoria_desc = obtener_descripcion_categoria(categoria_id)
        if categoria_desc in categorias_productos:
            categorias_productos[categoria_desc] += 1
        else:
            categorias_productos[categoria_desc] = 1

    # Se utiliza para preparar los datos para meterlos en el grafico 
    categorias = list(categorias_productos.keys())
    cantidad_productos = list(categorias_productos.values())

    # Crear el gráfico
    fig = plt.Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(categorias, cantidad_productos)

    # Configurar el gráfico
    ax.set_title('Cantidad de Productos por Categoría')
    ax.set_ylabel('Cantidad de Productos')
    ax.tick_params(axis='x', rotation=45)

    # Mostrar el gráfico en la ventana de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
def obtener_descripcion_categoria(categoria_id):
    my_database = my_client.Inventario
    roductoscollection = my_database['Productos']
    Categoriascollection = my_database['Categorias']
    categoria = Categoriascollection.find_one({'id_categoria': categoria_id})
    if categoria:
        return categoria['categoria_descripcion']
    else:
        return 'Desconocido'
def crear_ventanaGraficoCategorias():
    ventanaGraficoCategorias = tk.Tk()
    ventanaGraficoCategorias.title("Gráfico de Cantidad de Productos por Categoría")
    ventanaGraficoCategorias.geometry("500x800+500+350")
    # Llamar a la función para crear el gráfico
    crear_graficoCategorias(ventanaGraficoCategorias)

    # Ejecutar el bucle de eventos de Tkinter
    ventanaGraficoCategorias.mainloop()

# Funciones para CREAR VENTANA Y GRAFICO REPORTES
def crear_grafico_Reportes(master):
    # Consultar la base de datos para contar la cantidad de productos por mes
    my_database = my_client.Inventario
    Reportescollection = my_database['Reportes']
    productos_por_mes = defaultdict(int)
    for reporte in Reportescollection.find():
        fecha = reporte['fecha']
        mes = obtener_mes(fecha)
        productos_por_mes[mes] += 1

    # Preparar los datos para el gráfico
    meses = sorted(productos_por_mes.keys())
    cantidad_productos = [productos_por_mes[mes] for mes in meses]

    # Convertir el número de mes a nombre del mes
    nombres_meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    meses_con_nombre = [nombres_meses[mes-1] for mes in meses]

    # Crear el gráfico
    fig = plt.Figure(figsize=(6, 5), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(meses_con_nombre, cantidad_productos)

    # Configurar el gráfico
    ax.set_title('Cantidad de Productos Reportados por mes ')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Cantidad de Productos')

    # Mostrar el gráfico en la ventana de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
def obtener_mes(fecha):
    # Función para obtener el mes a partir de una fecha
    return fecha.month
def crear_ventanaGraficoReportes():
    ventanaGraficoReportes = tk.Tk()
    ventanaGraficoReportes.title("Gráfico de Cantidad de Reportados Productos por Mes")
    ventanaGraficoReportes.geometry("500x800+500+250")

    # Llamar a la función para crear el gráfico
    crear_grafico_Reportes(ventanaGraficoReportes)

    # Ejecutar el bucle de eventos de Tkinter
    ventanaGraficoReportes.mainloop()

#Funciones para CREAR VENTANA y GRAFICO ALMACENES
def crear_grafico_almacenes(master):
    my_database = my_client.Inventario
    Almacencollection = my_database['Almacen']
    
    # Sumar las cantidades de productos para cada almacén
    cantidad_por_almacen = defaultdict(int)
    for almacen in Almacencollection.find():
        localizacion = almacen['localizacion']
        cantidad = int(almacen['cantidad'])  # Convertir a entero
        cantidad_por_almacen[localizacion] += cantidad


    # Preparar los datos para el gráfico
    almacenes = list(cantidad_por_almacen.keys())
    cantidad_productos = list(cantidad_por_almacen.values())

    # Crear el gráfico
    fig = plt.Figure(figsize=(6, 5), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(almacenes, cantidad_productos)

    # Configurar el gráfico
    ax.set_title('Cantidad de Productos por Almacén')
    ax.set_ylabel('Cantidad de Productos')
    ax.tick_params(axis='x', rotation=45)

    # Mostrar el gráfico en la ventana de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
def crear_ventanaGraficoAlmacenes():
    ventanaGraficoAlmacenes = tk.Tk()
    ventanaGraficoAlmacenes.title("Gráfico de Cantidad de Productos por Almacén")
    ventanaGraficoAlmacenes.geometry("500x800+500+250")
    # Llamar a la función para crear el gráfico
    crear_grafico_almacenes(ventanaGraficoAlmacenes)

    # Ejecutar el bucle de eventos de Tkinter
    ventanaGraficoAlmacenes.mainloop()

# Funciones para crear ventana y gráfico PROVEEDORES
def crear_grafico_proveedores(master):
    my_database = my_client.Inventario
    Productoscollection = my_database['Productos']
    Proveedorescollection = my_database['Proveedor']
    
    # Se utiliza para obtener la cantidad de productos por proveedor
    proveedores_productos = defaultdict(int)
    for producto in Productoscollection.find():
        proveedor_id = producto['id_proveedor']
        proveedor_desc = obtener_descripcion_proveedor(proveedor_id)
        proveedores_productos[proveedor_desc] += 1

    # Se utiliza para preparar los datos para el gráfico
    proveedores = list(proveedores_productos.keys())
    cantidad_productos = list(proveedores_productos.values())

    # Crear el gráfico
    fig = plt.Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(proveedores, cantidad_productos)

    # Configurar el gráfico
    ax.set_title('Cantidad de Modelo de Productos por Proveedor')
    ax.set_ylabel('Cantidad de Modelos de Productos')
    ax.tick_params(axis='x', rotation=45)

    # Mostrar el gráfico en la ventana de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
def obtener_descripcion_proveedor(proveedor_id):
    my_database = my_client.Inventario
    Productoscollection = my_database['Productos']
    Proveedorescollection = my_database['Proveedor']
    proveedor = Proveedorescollection.find_one({'id_proveedor': proveedor_id})
    if proveedor:
        return proveedor['proveedor_descripcion']
    else:
        return 'Desconocido'
def crear_ventana_grafico_proveedores():
    ventana_proveedores = tk.Tk()
    ventana_proveedores.title("Gráfico de Cantidad de Productos por Proveedor")
    ventana_proveedores.geometry("500x800+500+250")

    # Llamar a la función para crear el gráfico
    crear_grafico_proveedores(ventana_proveedores)

    # Ejecutar el bucle de eventos de Tkinter
    ventana_proveedores.mainloop()

# Funciones para crear ventana  y grafico ROLES
def crear_grafico_roles(master):
    my_database = my_client.Inventario
    UsuarioCollection = my_database['Usuario']
    RolesCollection = my_database['Roles']

    # Obtener la cantidad de usuarios por rol
    usuarios_por_rol = defaultdict(int)
    for usuario in UsuarioCollection.find():
        rol_id = usuario['id_rol']
        rol_desc = obtener_descripcion_rol(rol_id)
        usuarios_por_rol[rol_desc] += 1

    # Preparar los datos para el gráfico
    roles = list(usuarios_por_rol.keys())
    cantidad_usuarios = list(usuarios_por_rol.values())

    # Crear el gráfico
    fig = plt.Figure(figsize=(6, 5), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(roles, cantidad_usuarios)

    # Configurar el gráfico
    ax.set_title('Cantidad de Usuarios por Rol')
    ax.set_ylabel('Cantidad de Usuarios')
    ax.tick_params(axis='x', rotation=45)

    # Formatear el eje y como enteros
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))

    # Mostrar el gráfico en la ventana de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
def obtener_descripcion_rol(rol_id):
    my_database = my_client.Inventario
    UsuarioCollection = my_database['Usuario']
    RolesCollection = my_database['Roles']  
    rol = RolesCollection.find_one({'id_rol': rol_id})
    if rol:
        return rol['rol_descripcion']
    else:
        return 'Desconocido'
def crear_ventana_grafico_roles():
    ventana_roles = tk.Tk()
    ventana_roles.title("Gráfico de Cantidad de Usuarios por Rol")
    ventana_roles.geometry("500x900+500+400")

    # Llamar a la función para crear el gráfico
    crear_grafico_roles(ventana_roles)

    # Ejecutar el bucle de eventos de Tkinter
    ventana_roles.mainloop()

#FUNCIONES DATA    
def categorias_data():

    my_database = my_client.Inventario
    mycollection = my_database['Categorias']
    
    # Fetch data from MongoDB
    data = mycollection.find({}, {"_id": 0, "categoria_descripcion": 1})   

    # Extract the values to populate in the dropdown
    options = [item['categoria_descripcion'] for item in data]

    return options

def proveedor_data():

    my_database = my_client.Inventario
    mycollection = my_database['Proveedor']

    # Fetch data from MongoDB
    data = mycollection.find({}, {"_id": 0, "proveedor_descripcion": 1})   

    # Extract the values to populate in the dropdown
    options = [item['proveedor_descripcion'] for item in data]

    return options

def productos_data():

    my_database = my_client.Inventario
    mycollection = my_database['Productos']

    # Fetch data from MongoDB
    data = mycollection.find({}, {"_id": 0, "nombre_producto": 1})   

    # Extract the values to populate in the dropdown
    options = [item['nombre_producto'] for item in data]

    return options

def roles_data():
    my_database = my_client.Inventario
    mycollection = my_database['Roles']

    # Fetch data from MongoDB
    data = mycollection.find({}, {"_id": 0, "rol_descripcion": 1})   

    # Extract the values to populate in the dropdown
    options = [item['rol_descripcion'] for item in data]


    return options

# Comparadores FUNCIONES PARA MANEJAR DATA PRUEBA 
def comparador_Proveedor(proveedor):
    my_database = my_client.Inventario
    mycollection = my_database['Proveedor']

    data = mycollection.find_one({"proveedor_descripcion": proveedor}, {"_id": 0, "id_proveedor": 1})  

    optionsid = data["id_proveedor"]

    return optionsid - 1

def comparador_Producto(productos):
    my_database = my_client.Inventario
    mycollection = my_database['Productos']

    data = mycollection.find_one({"nombre_producto": productos}, {"_id": 0, "id_producto": 1})  
 
    optionsid = data["id_producto"]

    return optionsid - 1

def comparador_Categorias(categorias):
    my_database = my_client.Inventario
    mycollection = my_database['Categorias']
    
    # Fetch data from MongoDB
    data = mycollection.find_one({"categoria_descripcion": categorias}, {"_id": 0, "id_categoria": 1})  

    # Extract the values to populate in the dropdown
    optionsid = data['id_categoria'] 

    return optionsid - 1

def comparador_Roles(roles):
    my_database= my_client.Inventario
    mycollection = my_database['Roles']

   # Fetch data from MongoDB
    data = mycollection.find_one({"rol_descripcion":roles}, {"_id": 0, "rol_descripcion": 1})   

    # Extract the values to populate in the dropdown
    optionsid = data['id_rol']


    return optionsid -1

# Función para mostrar la ventana emergente de creación
def ventana_crear_producto():
    ventana_crear_producto = tk.Toplevel()
    ventana_crear_producto.title("Crear Producto")
    ventana_crear_producto.geometry("250x300+600+200")
    ventana_crear_producto.resizable(True, True)
    
    # Etiqueta y entrada para el elemento a crear
    tk.Label(ventana_crear_producto, text="Nombre del Producto:").pack()
    entry_nombre = tk.Entry(ventana_crear_producto)
    entry_nombre.pack()

    tk.Label(ventana_crear_producto, text="Descripcion:").pack()
    entry_descripcion = tk.Entry(ventana_crear_producto)
    entry_descripcion.pack()

    tk.Label(ventana_crear_producto, text="Precio:").pack()
    entry_precio = tk.Entry(ventana_crear_producto)
    entry_precio.pack()

    tk.Label(ventana_crear_producto, text="Proveedor:").pack()
    options = proveedor_data()
    dropdown_prov = tk.StringVar(ventana_crear_producto)
    dropdown_prov.set(options[0])  # Set default value
    #  Crear Dropdown
    dropdownProv = tk.OptionMenu(ventana_crear_producto, dropdown_prov, *options)
    dropdownProv.pack()

    tk.Label(ventana_crear_producto, text="Categoria:").pack()
    options = categorias_data()
    dropdown_var = tk.StringVar(ventana_crear_producto)
    dropdown_var.set(options[0])  # Set default value
    #  Crear Dropdown
    dropdownCat = tk.OptionMenu(ventana_crear_producto, dropdown_var, *options)
    dropdownCat.pack()
    
    # Botón para confirmar la creación
    def confirmar_creacion():

        my_database = my_client.Inventario
        producto_collection = my_database['Productos']
        categorias_collection = my_database['Categorias']
        proveedor_collection = my_database['Proveedor']
        descripcion_collection = my_database['Descripcion']

        select_id_cat =  dropdown_var.get()
        resultadoCategoria = categorias_collection.find_one({"categoria_descripcion": select_id_cat})
        categoriaId =  resultadoCategoria["id_categoria"]

        select_id_prov =  dropdown_prov.get()
        resultadoProveedor = proveedor_collection.find_one({"proveedor_descripcion": select_id_prov})
        proveedorId =  resultadoProveedor["id_proveedor"]

        productoNombre = entry_nombre.get()

        productoID = 1 

        producto_id_cursor = producto_collection.find({})
        for item in producto_id_cursor:
           if (item["id_producto"] >= productoID):
              productoID = item["id_producto"] + 1

        descripcionID = 1 
        descripcion_id_cursor = descripcion_collection.find({})
        for item in descripcion_id_cursor:
           if (item["id_descripcion"] >= descripcionID):
              descripcionID = item["id_descripcion"] + 1       

        producto_collection.insert_one({
            "id_producto":  productoID,
            "id_descripcion": descripcionID,
            "nombre_producto" : productoNombre,
            "id_categoria": categoriaId,
            "id_proveedor": proveedorId,
            "fecha_ingreso" : datetime.datetime.now()
             })
        
        descripcion_collection.insert_one({
            "id_descripcion":  descripcionID,
            "producto_descripcion": entry_descripcion.get(),
            "precio" : entry_precio.get() 
             })

        messagebox.showinfo("Creado exitosamente", f"Producto \"{productoNombre}\" creado con éxito")
        ventana_crear_producto.destroy()  # Cerrar la ventana de creación
    
    boton_confirmar = tk.Button(ventana_crear_producto, text="Crear", command=confirmar_creacion)
    boton_confirmar.pack(pady=10)
def ventana_crear_proveedor():
    ventana_crear_proveedor = tk.Toplevel()
    ventana_crear_proveedor.title("Crear Proveedor")
    ventana_crear_proveedor.geometry("250x100+600+200")
    ventana_crear_proveedor.resizable(True, True)
    
    # Etiqueta y entrada para el elemento a crear
    tk.Label(ventana_crear_proveedor, text="Nombre del Proveedor:").pack()
    entry_nombre = tk.Entry(ventana_crear_proveedor)
    entry_nombre.pack()
    
    # Botón para confirmar la creación
    def confirmar_creacion_prov():

        my_database = my_client.Inventario
        proveedor_collection = my_database['Proveedor']

        proveedorNombre = entry_nombre.get()

        proveedorID = 1 

        proveedor_id_cursor = proveedor_collection.find({})
        for item in proveedor_id_cursor:
           if (item["id_proveedor"] >= proveedorID):
              proveedorID = item["id_proveedor"] + 1
  
        proveedor_collection.insert_one({
            "id_proveedor":  proveedorID,
            "proveedor_descripcion": proveedorNombre
             })

        messagebox.showinfo("Creado exitosamente", f"Proveedor \"{proveedorNombre}\" creado con éxito")
        ventana_crear_proveedor.destroy()  # Cerrar la ventana de creación
    
    boton_confirmar = tk.Button(ventana_crear_proveedor, text="Crear", command=confirmar_creacion_prov)
    boton_confirmar.pack(pady=10)
def ventana_crear_categoria():
    ventana_crear_categoria = tk.Toplevel()
    ventana_crear_categoria.title("Crear Categoria")
    ventana_crear_categoria.geometry("250x100+600+200")
    ventana_crear_categoria.resizable(True, True)
    
    # Etiqueta y entrada para el elemento a crear
    tk.Label(ventana_crear_categoria, text="Nombre de la Categoria:").pack()
    entry_categoria = tk.Entry(ventana_crear_categoria)
    entry_categoria.pack()
    
    # Botón para confirmar la creación
    def confirmar_creacion_cat():

        my_database = my_client.Inventario
        categoria_collection = my_database['Categorias']

        categoriaNombre = entry_categoria.get()

        categoriaID = 1 

        categoria_id_cursor = categoria_collection.find({})
        for item in categoria_id_cursor:
           if (item["id_categoria"] >= categoriaID):
              categoriaID = item["id_categoria"] + 1
  
        categoria_collection.insert_one({
            "id_categoria":  categoriaID,
            "categoria_descripcion": categoriaNombre
             })

        messagebox.showinfo("Creado exitosamente", f"Categoria \"{categoriaNombre}\" creada con éxito")
        ventana_crear_categoria.destroy()  # Cerrar la ventana de creación
    
    boton_confirmar = tk.Button(ventana_crear_categoria, text="Crear", command=confirmar_creacion_cat)
    boton_confirmar.pack(pady=10)
def ventana_crear_almacen():
    ventana_crear_almacen = tk.Toplevel()
    ventana_crear_almacen.title("Crear Almacen")
    ventana_crear_almacen.geometry("250x250+600+200")
    ventana_crear_almacen.resizable(True, True)
    
    # Etiqueta y entrada para el elemento a crear
    tk.Label(ventana_crear_almacen, text="Nombre del Almacen:").pack()
    entry_nombre = tk.Entry(ventana_crear_almacen)
    entry_nombre.pack()

    tk.Label(ventana_crear_almacen, text="Localizacion:").pack()
    entry_localizacion = tk.Entry(ventana_crear_almacen)
    entry_localizacion.pack()

    tk.Label(ventana_crear_almacen, text="Producto Inicial:").pack()
    options = productos_data()
    dropdown_var = tk.StringVar(ventana_crear_almacen)
    dropdown_var.set(options[0])  # Set default value
    #  Crear Dropdown
    dropdownCat = tk.OptionMenu(ventana_crear_almacen, dropdown_var, *options)
    dropdownCat.pack()

    tk.Label(ventana_crear_almacen, text="Cantidad Inicial:").pack()
    entry_cantidad = tk.Entry(ventana_crear_almacen)
    entry_cantidad.pack()

    # Botón para confirmar la creación
    def confirmar_creacion():

        my_database = my_client.Inventario
        producto_collection = my_database['Productos']
        almacen_collection = my_database['Almacen']
        descripcion_collection = my_database['Descripcion']

        select_id_pro =  dropdown_var.get()
        resultadoProducto = producto_collection.find_one({"nombre_producto": select_id_pro})
        productoID =  resultadoProducto["id_producto"]

        almacenNombre = entry_nombre.get()
        almacenCantidad = entry_cantidad.get()
        almacenLocalizacion = entry_localizacion.get()

        almacenID = 1 

        almacen_id_cursor = almacen_collection.find({})
        for item in almacen_id_cursor:
           if (item["id_almacen"] >= almacenID):
              almacenID = item["id_almacen"] + 1

        almacen_collection.insert_one({
            "id_almacen":  almacenID,
            "id_producto":  productoID,
            "nombre_almacen": almacenNombre,
            "localizacion" : almacenLocalizacion,
            "cantidad": almacenCantidad 
             })
        
        messagebox.showinfo("Creado exitosamente", f"Almacen \"{almacenNombre}\" creado con éxito")
        ventana_crear_almacen.destroy()  # Cerrar la ventana de creación
    
    boton_confirmar = tk.Button(ventana_crear_almacen, text="Crear", command=confirmar_creacion)
    boton_confirmar.pack(pady=10)
    
def ventana_crear_usuario():
    ventana_crear_usuario = tk.Toplevel()
    ventana_crear_usuario.title("Crear Usuario")
    ventana_crear_usuario.geometry("250x350+600+200")
    ventana_crear_usuario.resizable(True, True)
    
    # Etiqueta y entrada para el elemento a crear
    tk.Label(ventana_crear_usuario, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana_crear_usuario)
    entry_nombre.pack()

    tk.Label(ventana_crear_usuario, text="Primer Apellido:").pack()
    entry_apellido1 = tk.Entry(ventana_crear_usuario)
    entry_apellido1.pack()

    tk.Label(ventana_crear_usuario, text="Segundo Apellido:").pack()
    entry_apellido2 = tk.Entry(ventana_crear_usuario)
    entry_apellido2.pack()

    tk.Label(ventana_crear_usuario, text="Email:").pack()
    entry_email = tk.Entry(ventana_crear_usuario)
    entry_email.pack()

    tk.Label(ventana_crear_usuario, text="Contraseña:").pack()
    entry_contrasena = tk.Entry(ventana_crear_usuario, show="*")
    entry_contrasena.pack()

    tk.Label(ventana_crear_usuario, text="Confirmar Contraseña:").pack()
    entry_contrasenaConf = tk.Entry(ventana_crear_usuario, show="*")
    entry_contrasenaConf.pack()

    tk.Label(ventana_crear_usuario, text="Rol:").pack()
    options = roles_data()
    dropdown_var = tk.StringVar(ventana_crear_usuario)
    dropdown_var.set(options[0])  # Set default value
    #  Crear Dropdown
    dropdownRol = tk.OptionMenu(ventana_crear_usuario, dropdown_var, *options)
    dropdownRol.pack()
    
    # Botón para confirmar la creación
    def confirmar_creacion_usua():

        my_database = my_client.Inventario
        usuario_collection = my_database['Usuario']
        roles_collection = my_database['Roles']

        select_id_rol =  dropdown_var.get()
        resultadoRol = roles_collection.find_one({"rol_descripcion": select_id_rol})
        rolId =  resultadoRol["id_rol"]

        usuarioNombre = entry_nombre.get()
        usuarioApellido1 = entry_apellido1.get()
        usuarioApellido2 = entry_apellido2.get()
        usuarioContrasena = entry_contrasena.get()

        usuarioEmail = entry_email.get()

        usuarioID = 1 

        usuario_id_cursor = usuario_collection.find({})
        for item in usuario_id_cursor:
           if (item["id_usuario"] >= usuarioID):
              usuarioID = item["id_usuario"] + 1  

        usuario_collection.insert_one({
            "id_usuario":  usuarioID,
            "nombre": usuarioNombre,
            "apellido1" : usuarioApellido1,
            "apellido2": usuarioApellido2,
            "contraseña": usuarioContrasena,
            "email" : usuarioEmail,
            "id_rol" : rolId
             })
        
        messagebox.showinfo("Creado exitosamente", f"Usuario: \"{usuarioNombre} {usuarioApellido1}\" creado")
        ventana_crear_usuario.destroy()  # Cerrar la ventana de creación
    
    boton_confirmar = tk.Button(ventana_crear_usuario, text="Crear", command=confirmar_creacion_usua)
    boton_confirmar.pack(pady=10)

#EDITAR VENTANAS 

def ventana_editar_usuario(id_usuario,nombre_usuarios,apellido1_usuarios,apellido2_usuarios,email_usuarios,rol_usuarios):
    my_database = my_client.Inventario
    rol_collection = my_database['Roles']
    usuario_collection = my_database['Usuario']

    ventana_editar_usua = tk.Toplevel()
    ventana_editar_usua.title("Editar Usuario")
    ventana_editar_usua.geometry("200x400+600+200")
    ventana_editar_usua.resizable(True, True)
    
    # Etiqueta y entrada para el elemento a editar
    tk.Label(ventana_editar_usua, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana_editar_usua)
    entry_nombre.insert(0,nombre_usuarios)
    entry_nombre.pack()
 
    tk.Label(ventana_editar_usua, text="Primer Apellido:").pack()
    entry_apellido1 = tk.Entry(ventana_editar_usua)
    entry_apellido1.insert(0,apellido1_usuarios)
    entry_apellido1.pack()
 
    tk.Label(ventana_editar_usua, text="Segundo Apellido:").pack()
    entry_apellido2 = tk.Entry(ventana_editar_usua)
    entry_apellido2.insert(0,apellido2_usuarios)
    entry_apellido2.pack()
 
    tk.Label(ventana_editar_usua, text="Email:").pack()
    entry_email = tk.Entry(ventana_editar_usua)
    entry_email.insert(0,email_usuarios)
    entry_email.pack()
 
    tk.Label(ventana_editar_usua, text="Contraseña:").pack()
    entry_contrasena = tk.Entry(ventana_editar_usua, show="*")
    entry_contrasena.pack()
 
    tk.Label(ventana_editar_usua, text="Rol:").pack()
    options = roles_data()
    dropdown_rol = tk.StringVar(ventana_editar_usua)
    roles = int(rol_usuarios)
    dropdown_rol.set(options[roles-1])  # Set default value
    #  Crear Dropdown
    dropdownRol = tk.OptionMenu(ventana_editar_usua, dropdown_rol, *options)
    dropdownRol.pack()
 
    # Botón para confirmar la edición
    def confirmar_edicion():
        my_database = my_client.Inventario
        usuario_collection = my_database['Usuario']
        rol_collection = my_database['Roles']

        select_id_cat =  dropdown_rol.get()
        resultadoCategoria = rol_collection.find_one({"rol_descripcion": select_id_cat})
        idRol =  resultadoCategoria["id_rol"]
     
        usuarioNombre=entry_nombre.get()
       
        usuario_collection.update_one({"id_usuario":  id_usuario},{"$set":{
                "nombre": entry_nombre.get(),
                "apellido1" : entry_apellido1.get(),
                "apellido2" : entry_apellido2.get(),
                "contraseña" : entry_contrasena.get(),
                "email" : entry_email.get(),
                "id_rol" : idRol
                 }})
        
        

        messagebox.showinfo("Editado exitosamente", f"  Usuario \"{usuarioNombre}\" editada con éxito")
        ventana_editar_usua.destroy()
        manejar_opcion_ver_usuarios() #ACTUALIZA LA TABLA

    # Cerrar la ventana de edición  
    def borrar_usuario():
        my_database = my_client.Inventario
        usuario_collection = my_database['Usuario']
 
        usuario_collection.delete_one({"id_usuario":  id_usuario})
        messagebox.showinfo("Borrado exitosamente", f"  Usuario \"{nombre_usuarios}\" borrado con éxito")
        ventana_editar_usua.destroy()  # Cerrar la ventana de edición
        manejar_opcion_ver_usuarios()
 
    #BOTONES DE VENTANA EDITAR Usuario    
    boton_confirmar = tk.Button(ventana_editar_usua, text="Guardar", command=confirmar_edicion,bg="green",fg="white")
    boton_confirmar.pack(side="left", padx=25, pady=15)
 
    boton_borrar = tk.Button(ventana_editar_usua, text="Borrar", command=borrar_usuario,bg="red", fg= "white")
    boton_borrar.pack(side="right", padx=25, pady=10)
def ventana_editar_almacen(id_almacen,nombre_almacen, nombre_producto,localizacion,cantidad):
 
    ventana_editar_alma = tk.Toplevel()
    ventana_editar_alma.title("Editar Almacen")
    ventana_editar_alma.geometry("350x250+600+200")
    ventana_editar_alma.resizable(True, True)

    tk.Label(ventana_editar_alma, text="Nombre del Almacen:").pack()
    entry_nombre = tk.Entry(ventana_editar_alma, width=30)
    entry_nombre.insert(0, nombre_almacen)
    entry_nombre.pack()

    tk.Label(ventana_editar_alma, text="Localizacion:").pack()
    entry_localizacion = tk.Entry(ventana_editar_alma, width=30)
    entry_localizacion.insert(0,localizacion)
    entry_localizacion.pack()

    tk.Label(ventana_editar_alma, text="Producto:").pack()
    idproducto= comparador_Producto(nombre_producto)
    options = productos_data()
    dropdown_prov = tk.StringVar(ventana_editar_alma)
    dropdown_prov.set(options[idproducto])  # Set default value
    #  Crear Dropdown
    dropdownProv = tk.OptionMenu(ventana_editar_alma, dropdown_prov, *options)
    dropdownProv.pack()

    tk.Label(ventana_editar_alma, text="Cantidad Disponible:").pack()
    entry_cantidad = tk.Entry(ventana_editar_alma, width=20)
    entry_cantidad.insert(0,cantidad)
    entry_cantidad.pack()
 
    # Botón para confirmar la edición
    def confirmar_edicion():
        my_database = my_client.Inventario
        producto_collection = my_database['Productos']
        almacen_collection = my_database['Almacen']

        select_id_prov =  dropdown_prov.get()
        resultadoProducto = producto_collection.find_one({"nombre_producto": select_id_prov})
        productoId =  resultadoProducto["id_producto"]

        almaNombre = entry_nombre.get()
        cantidadAlma = entry_cantidad.get()
        localizacionAlma = entry_localizacion.get()

        almacen_collection.update_one({"id_almacen":id_almacen},{"$set":{
            "id_producto": productoId,
            "nombre_almacen" : almaNombre,
            "localizacion": localizacionAlma,
            "cantidad": cantidadAlma
             }})
        
        messagebox.showinfo("Editado exitosamente", f"Almacen \"{almaNombre}\" fue editado con éxito")
        ventana_editar_alma.destroy() 
        manejar_opcion_ver_almacen() #ACTUALIZA LA TABLA
        
         # Cerrar la ventana de edición  
    def borrar_producto():
        my_database = my_client.Inventario
        almacen_collection = my_database['Almacen']
   
        almacen_collection.delete_one({"id_almacen":  id_almacen})
        messagebox.showinfo("Borrado exitosamente", f"Almacen \"{nombre_almacen}\" fue borrado con éxito")
        ventana_editar_alma.destroy()  # Cerrar la ventana de edición
        manejar_opcion_ver_almacen()

    #BOTONES DE VENTANA EDITAR PRODUCTO     
    boton_confirmar = tk.Button(ventana_editar_alma, text="Guardar", command=confirmar_edicion,bg="green",fg="white")
    boton_confirmar.pack(side="left", padx=25, pady=15)

    boton_borrar = tk.Button(ventana_editar_alma, text="Borrar", command=borrar_producto, bg="red", fg= "white")
    boton_borrar.pack(side="right", padx=25, pady=10)
def ventana_editar_proveedor(id_proveedor,proveedor_descripcion):
     
    ventana_editar_prov = tk.Toplevel()
    ventana_editar_prov.title("Editar Proveedor")
    ventana_editar_prov.geometry("300x150+600+200")
    ventana_editar_prov.resizable(True, True)

    tk.Label(ventana_editar_prov, text="ID del Proveedor:").pack()
    entry_id = tk.Entry(ventana_editar_prov, width=30)
    entry_id.insert(0, id_proveedor)
    entry_id.pack()

    tk.Label(ventana_editar_prov, text="Nombre del Proveedor:").pack()
    entry_descripcion = tk.Entry(ventana_editar_prov, width=30)
    entry_descripcion.insert(0,proveedor_descripcion)
    entry_descripcion.pack()
 
    # Botón para confirmar la edición
    def confirmar_edicion():
        my_database = my_client.Inventario
        proveedor_collection = my_database['Proveedor']
 
        proveedorID = int(entry_id.get())
        proveedorDescripcion = entry_descripcion.get()
               
        proveedor_collection.update_one({"id_proveedor": id_proveedor},{"$set":{ "id_proveedor": proveedorID, 
                "proveedor_descripcion": proveedorDescripcion
                 }})  
        
        messagebox.showinfo("Editado exitosamente", f"Proveedor \"{proveedorDescripcion}\" editada con éxito")
        ventana_editar_prov.destroy() 
        manejar_opcion_ver_proveedores() #ACTUALIZA LA TABLA
        
         # Cerrar la ventana de edición  
    def borrar_proveedor():
        my_database = my_client.Inventario
        proveedor_collection = my_database['Proveedor']

        proveedor_collection.delete_one({"id_proveedor":  id_proveedor})
        messagebox.showinfo("Borrado exitosamente", f"Proveedor \"{proveedor_descripcion}\" borrado con éxito")
        ventana_editar_prov.destroy()  # Cerrar la ventana de edición
        manejar_opcion_ver_proveedores()

    #BOTONES DE VENTANA EDITAR PRODUCTO     
    boton_confirmar = tk.Button(ventana_editar_prov, text="Guardar", command=confirmar_edicion,bg="green",fg="white")
    boton_confirmar.pack(side="left", padx=25, pady=15)

    boton_borrar = tk.Button(ventana_editar_prov, text="Borrar", command=borrar_proveedor, bg="red", fg= "white")
    boton_borrar.pack(side="right", padx=25, pady=10)
def ventana_editar_categoria(id_categoria,categoria_descripcion):
     
    ventana_editar_categoria = tk.Toplevel()
    ventana_editar_categoria.title("Editar Categoria")
    ventana_editar_categoria.geometry("400x300+600+200")
    ventana_editar_categoria.resizable(True, True)

    tk.Label(ventana_editar_categoria, text="ID de Categoria:").pack()
    entry_id = tk.Entry(ventana_editar_categoria, width=50)
    entry_id.insert(0, id_categoria)
    entry_id.pack()

    tk.Label(ventana_editar_categoria, text="Descripcion de la Categoria:").pack()
    entry_descripcion = tk.Entry(ventana_editar_categoria, width=50)
    entry_descripcion.insert(0,categoria_descripcion)
    entry_descripcion.pack()
 
    # Botón para confirmar la edición
    def confirmar_edicion():
        my_database = my_client.Inventario
        categorias_collection = my_database['Categorias']
 
        categoriaID = int(entry_id.get())
        categoriaDescripcion = entry_descripcion.get()
               
        categorias_collection.update_one({"id_categoria": id_categoria},{"$set":{ "id_categoria": categoriaID, 
                "categoria_descripcion": categoriaDescripcion
                 }})  
        
        messagebox.showinfo("Editado exitosamente", f"Categoria \"{categoriaDescripcion}\" editada con éxito")
        ventana_editar_categoria.destroy() 
        manejar_opcion_ver_categorias() #ACTUALIZA LA TABLA
        
         # Cerrar la ventana de edición  
    def borrar_producto():
        my_database = my_client.Inventario
        categorias_collection = my_database['Categorias']

        categorias_collection.delete_one({"id_categoria":  id_categoria})
        messagebox.showinfo("Borrado exitosamente", f"Categoria \"{categoria_descripcion}\" borrada con éxito")
        ventana_editar_categoria.destroy()  # Cerrar la ventana de edición
        manejar_opcion_ver_categorias()

    #BOTONES DE VENTANA EDITAR PRODUCTO     
    boton_confirmar = tk.Button(ventana_editar_categoria, text="Guardar", command=confirmar_edicion,bg="green",fg="white")
    boton_confirmar.pack(side="left", padx=25, pady=15)

    boton_borrar = tk.Button(ventana_editar_categoria, text="Borrar", command=borrar_producto, bg="red", fg= "white")
    boton_borrar.pack(side="right", padx=25, pady=10)
def ventana_editar_producto(id_producto,nombre_producto,descripcion_producto,precio_producto,proovedor_producto,categorias_producto,fechaIngreso_producto):
    my_database = my_client.Inventario
    producto_collection = my_database['Productos']
    categorias_collection = my_database['Categorias']
    proveedor_collection = my_database['Proveedor']
    descripcion_collection = my_database['Descripcion']
    
    ventana_editar_producto = tk.Toplevel()
    ventana_editar_producto.title("Editar Producto")
    ventana_editar_producto.geometry("400x300+600+200")
    ventana_editar_producto.resizable(True, True)

    # Etiqueta y entrada para el elemento a editar
    #NPData= mycollection.find_one({"id_producto":producto_actual},{"_id":0,"nombre_producto":1})
    #nombreProducto= NPData['nombre_producto']

    tk.Label(ventana_editar_producto, text="Nombre del Producto:").pack()
    entry_nombre = tk.Entry(ventana_editar_producto, width=50)
    entry_nombre.insert(0, nombre_producto)
    entry_nombre.pack()

    tk.Label(ventana_editar_producto, text="Descripcion:").pack()
    entry_descripcion = tk.Entry(ventana_editar_producto, width=50)
    entry_descripcion.insert(0,descripcion_producto)
    entry_descripcion.pack()

    tk.Label(ventana_editar_producto, text="Precio:").pack()
    entry_precio = tk.Entry(ventana_editar_producto, width=20)
    entry_precio.insert(0,precio_producto)
    entry_precio.pack()

    tk.Label(ventana_editar_producto, text="Proveedor:").pack()
    idproveedor= comparador_Proveedor(proovedor_producto)
    options = proveedor_data()
    dropdown_prov = tk.StringVar(ventana_editar_producto)
    dropdown_prov.set(options[idproveedor])  # Set default value
    #  Crear Dropdown
    dropdownProv = tk.OptionMenu(ventana_editar_producto, dropdown_prov, *options)
    dropdownProv.pack()

    tk.Label(ventana_editar_producto, text="Categoria:").pack()
    idcategorias= comparador_Categorias(categorias_producto)
    options = categorias_data()
    dropdown_cat = tk.StringVar(ventana_editar_producto)
    dropdown_cat.set(options[idcategorias])  # Set default value
    #  Crear Dropdown
    dropdownCat = tk.OptionMenu(ventana_editar_producto, dropdown_cat, *options)
    dropdownCat.pack()
    
    # Botón para confirmar la edición
    def confirmar_edicion():
        my_database = my_client.Inventario
        producto_collection = my_database['Productos']
        categorias_collection = my_database['Categorias']
        proveedor_collection = my_database['Proveedor']
        descripcion_collection = my_database['Descripcion']

        select_id_cat =  dropdown_cat.get()
        resultadoCategoria = categorias_collection.find_one({"categoria_descripcion": select_id_cat})
        categoriaId =  resultadoCategoria["id_categoria"]

        select_id_prov =  dropdown_prov.get()
        resultadoProveedor = proveedor_collection.find_one({"proveedor_descripcion": select_id_prov})
        proveedorId =  resultadoProveedor["id_proveedor"]

        productoNombre = entry_nombre.get()

        descripcion_collection.update_one({"id_descripcion":  id_producto},{"$set":{
                "producto_descripcion": entry_descripcion.get(),
                "precio" : entry_precio.get() 
                 }})

        producto_collection.update_one({"id_producto":id_producto},{"$set":{
            "nombre_producto" : productoNombre,
            "id_categoria": categoriaId,
            "id_proveedor": proveedorId,
             }})
        
        messagebox.showinfo("Editado exitosamente", f"Producto \"{productoNombre}\" editado con éxito")
        ventana_editar_producto.destroy() 
        manejar_opcion_ver_productos() #ACTUALIZA LA TABLA
        
         # Cerrar la ventana de edición  
    def borrar_producto():
        my_database = my_client.Inventario
        producto_collection = my_database['Productos']
        descripcion_collection = my_database['Descripcion']

        descripcion_collection.delete_one({"id_descripcion":  id_producto})
        producto_collection.delete_one({"id_producto":  id_producto})
        messagebox.showinfo("Borrado exitosamente", f"Producto \"{nombre_producto}\" borrado con éxito")
        ventana_editar_producto.destroy()  # Cerrar la ventana de edición
        manejar_opcion_ver_productos()

    #BOTONES DE VENTANA EDITAR PRODUCTO     
    boton_confirmar = tk.Button(ventana_editar_producto, text="Guardar", command=confirmar_edicion,bg="green",fg="white")
    boton_confirmar.pack(side="left", padx=25, pady=15)

    boton_borrar = tk.Button(ventana_editar_producto, text="Borrar", command=borrar_producto, bg="red", fg= "white")
    boton_borrar.pack(side="right", padx=25, pady=10)

def ventana_editar_reporte(id_reporte,fecha,id_producto):
   my_database= my_client.Inventario
   reporte_collection = my_database['Reportes']
   producto_collection = my_database['Productos']

   ventana_editar_rep = tk.Toplevel()
   ventana_editar_rep.title("Editar Reporte")
   ventana_editar_rep.geometry("300x200+600+200")
   ventana_editar_rep.resizable(True, True)

   # Etiqueta y entrada para el elemento a editar


   tk.Label(ventana_editar_rep, text="Producto:").pack()
   id_producto = id_producto -1
   options = productos_data()
   dropdown_rep = tk.StringVar(ventana_editar_rep)
   dropdown_rep.set(options[id_producto])  # Set default value
   #  Crear Dropdown
   dropdownRol = tk.OptionMenu(ventana_editar_rep, dropdown_rep, *options)
   dropdownRol.pack()
   
   def confirmar_edicion():
        my_database= my_client.Inventario
        reporte_collection = my_database['Reportes']
        producto_collection = my_database['Productos']

        select_id_rep =  dropdown_rep.get()
        resultadoProducto = producto_collection.find_one({"nombre_producto": select_id_rep})
        idProd =  resultadoProducto["id_producto"]
     
        reporte_collection.update_one({"id_reporte":id_reporte},{"$set":{
                "id_producto": idProd
                }})
        
        messagebox.showinfo("Editado exitosamente", f" Reporte con el id  \"{id_reporte}\" editada con éxito")
        ventana_editar_rep.destroy()
        manejar_opcion_ver_reportes()

   def borrar_reporte():
      my_database = my_client.Inventario
      reporte_collection = my_database['Reportes']
      reporte_collection.delete_one({"id_reporte":  id_reporte})
      messagebox.showinfo("Borrado exitosamente", f"  Reporte con el id  \"{id_reporte}\" borrado con éxito")
      ventana_editar_rep.destroy()  # Cerrar la ventana de edición
      manejar_opcion_ver_reportes()
   
   boton_confirmar = tk.Button(ventana_editar_rep, text="Guardar", command=confirmar_edicion,bg="green",fg="white")
   boton_confirmar.pack(side="left", padx=25, pady=15)

   boton_borrar = tk.Button(ventana_editar_rep, text="Borrar", command=borrar_reporte, bg="red", fg= "white")
   boton_borrar.pack(side="right", padx=25, pady=10)


#OPCIONES de PERFIL
def ventana_cambiar_clave():
 
    ventana_clave = tk.Toplevel()
    ventana_clave.title("Cambiar Clave")
    ventana_clave.geometry("250x200+600+200")
    ventana_clave.resizable(True, True)
    
    # Etiqueta y entrada para el elemento a editar
    tk.Label(ventana_clave, text="Contraseña Actual:").pack()
    entry_clave1 = tk.Entry(ventana_clave, show="*")
    entry_clave1.pack()

    # Etiqueta y entrada para el elemento a editar
    tk.Label(ventana_clave, text="Confirmar Contraseña:").pack()
    entry_clave2 = tk.Entry(ventana_clave, show="*")
    entry_clave2.pack()
    
    tk.Label(ventana_clave, text="Nueva Contraseña:").pack()
    entry_nueva = tk.Entry(ventana_clave, show="*")
    entry_nueva.pack()
 
    # Botón para confirmar la edición
    def confirmar_edicion():
        my_database = my_client.Inventario
        usuario_collection = my_database['Usuario']
 
        email = email_activo
        contrasena1 =entry_clave1.get()
        contrasena2 = entry_clave2.get()
        nuevaContrasena = entry_nueva.get()

        resultadoContrasena = usuario_collection.find_one({"email": email})
        contrasenaDB =  resultadoContrasena["contraseña"]
       

        if (contrasena1 == contrasena2 and contrasena1 == contrasenaDB):
         usuario_collection.update_one({"email": email},{"$set":{
                "contraseña" : nuevaContrasena
                
                 }})
        

         messagebox.showinfo("Editado exitosamente", f"Contraseña editada con éxito")
         ventana_clave.destroy()

        else: 

         messagebox.showinfo("Datos Incorrectos", f"Por favor intentelo nuevamente")
         
 
    # Cerrar la ventana de edición  
    def cerrar_perfil():
 
        ventana_clave.destroy()  
    
    boton_guardar = tk.Button(ventana_clave, text="Guardar", command=confirmar_edicion,bg="green",fg="white")
    boton_guardar.pack(side="left", padx=25, pady=15)
 
    boton_cerrar = tk.Button(ventana_clave, text="Cerrar", command=cerrar_perfil, bg="red", fg= "white")  
    boton_cerrar.pack(side="right", padx=25, pady=10)
def ventana_cambiar_email():
 
    ventana_clave = tk.Toplevel()
    ventana_clave.title("Cambiar Email")
    ventana_clave.geometry("250x200+600+200")
    ventana_clave.resizable(True, True)
    
    tk.Label(ventana_clave, text="Nuevo Email:").pack()
    entry_email = tk.Entry(ventana_clave)
    entry_email.insert(0,email_activo)
    entry_email.pack()

    # Etiqueta y entrada para el elemento a editar
    tk.Label(ventana_clave, text="Contraseña:").pack()
    entry_clave1 = tk.Entry(ventana_clave, show="*")
    entry_clave1.pack()

    # Etiqueta y entrada para el elemento a editar
    tk.Label(ventana_clave, text="Confirmar Contraseña:").pack()
    entry_clave2 = tk.Entry(ventana_clave, show="*")
    entry_clave2.pack()
    
    email = email_activo

    # Botón para confirmar la edición
    def confirmar_edicion():
        my_database = my_client.Inventario
        usuario_collection = my_database['Usuario']
 
        contrasena1 =entry_clave1.get()
        contrasena2 = entry_clave2.get()
        nuevoEmail = entry_email.get()

        resultadoContrasena = usuario_collection.find_one({"email": email})
        contrasenaDB =  resultadoContrasena["contraseña"]
       
        if (contrasena1 == contrasena2 and contrasena1 == contrasenaDB):
         usuario_collection.update_one({"email": email},{"$set":{
                "email" : nuevoEmail
                 }})      
       
         messagebox.showinfo("Editado exitosamente", f"Email editado, por favor vuelva a ingresar")
         ventana_clave.destroy()
         
        else: 

         messagebox.showinfo("Datos no coinciden", f"Por favor intentelo nuevamente")
    
    # Cerrar la ventana de edición  
    def cerrar_perfil():
 
        ventana_clave.destroy()  # Cerrar la ventana de edición
 

    #BOTONES DE VENTANA EDITAR Usuario    
    boton_guardar = tk.Button(ventana_clave, text="Guardar", command=confirmar_edicion,bg="green",fg="white")
    boton_guardar.pack(side="left", padx=25, pady=15)
 
    boton_cerrar = tk.Button(ventana_clave, text="Cerrar", command=cerrar_perfil, bg="red", fg= "white")  
    boton_cerrar.pack(side="right", padx=25, pady=10)



#CERRAR SESSION
def cerrar_sesion():
    abrir_ventana_login()  # Volver a abrir la ventana de inicio de sesión



# Función para abrir la ventana principal después del inicio de sesión exitoso
def abrir_ventana_principal(rol_sesion, email_sesion):
    # Cerrar la ventana de inicio de sesión

    def cerrar_ventana_principal():
         ventana_principal.destroy()  # Cerrar la ventana principal
         cerrar_sesion()

    def mostrar_menu(event):
       menu_cuenta.post(event.x_root, event.y_root)
       boton_menu.config(relief=tk.RAISED)

    def restablecer_estado(event):
       boton_menu.config(relief=tk.RAISED)
   
    # Variables de Rol y Email de Sesión
    global rol_activo
    rol_activo = rol_sesion
    
    global email_activo
    email_activo = email_sesion
 
    # Crear la ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Inventario Tienda Gansito")
    ventana_principal.geometry("1000x650+150+150")
    ventana_principal.resizable(False, False)  # Evitar que la ventana cambie de tamaño
    
    # Configuración de colores y estilos
    color_fondo_principal = "white"
    color_texto_principal = "white"
    color_texto_principal2 = "black"
    fuente_texto_principal = ("Arial", 12, "bold")
    fuente_texto_principal2 = ("Arial", 14, "bold")
    color_boton_principal = "deepskyblue3"

    ventana_principal.configure(bg=color_fondo_principal)



    # Frame para los botones de "Ver"
    frame_ver = tk.Frame(ventana_principal, bg=color_fondo_principal)
    frame_ver.pack(anchor="w", padx=10, pady=5)

    label_ver = tk.Label(frame_ver, text="Ver", bg=color_fondo_principal, fg=color_texto_principal2, font=fuente_texto_principal2)
    label_ver.pack(side="left", padx=10, pady=5)

    menu_cuenta = Menu(frame_ver, tearoff=0, borderwidth=2, relief="solid")
    menu_cuenta.add_separator()
    menu_cuenta.add_command(label="Cambiar Contraseña", command=ventana_cambiar_clave)
    menu_cuenta.add_separator()
    menu_cuenta.add_command(label="Cambiar Email", command=ventana_cambiar_email)
    menu_cuenta.add_separator()
    menu_cuenta.add_command(label="Cerrar Sesión", command=cerrar_ventana_principal)
    menu_cuenta.add_separator()
    
    if (rol_activo == 1): 
     boton_usuarios = tk.Button(frame_ver, text="Usuarios", command=lambda: manejar_opcion_ver_usuarios(), bg=color_boton_principal, fg=color_texto_principal)
     boton_usuarios.pack(side="left", padx=20, pady=5)

     boton_roles = tk.Button(frame_ver, text="Roles", command=lambda: manejar_opcion_ver_roles(), bg=color_boton_principal, fg=color_texto_principal)
     boton_roles.pack(side="left", padx=20, pady=5)

    boton_proveedor = tk.Button(frame_ver, text="Proveedores", command=lambda: manejar_opcion_ver_proveedores(), bg=color_boton_principal, fg=color_texto_principal)
    boton_proveedor.pack(side="left", padx=20, pady=5)

    boton_almacen = tk.Button(frame_ver, text="Almacén", command=lambda: manejar_opcion_ver_almacen(), bg=color_boton_principal, fg=color_texto_principal)
    boton_almacen.pack(side="left", padx=20, pady=5)

    boton_productos = tk.Button(frame_ver, text="Productos", command=lambda: manejar_opcion_ver_productos(), bg=color_boton_principal, fg=color_texto_principal)
    boton_productos.pack(side="left", padx=20, pady=5)

    boton_reportes = tk.Button(frame_ver, text="Reportes", command=lambda: manejar_opcion_ver_reportes(), bg=color_boton_principal, fg=color_texto_principal)
    boton_reportes.pack(side="left", padx=20, pady=5)    

     #Configurar el botón de menú hamburguesa
    boton_menu = tk.Button(frame_ver, text="Cuenta ☰ ", bg="ivory3", fg="black", font=("Arial", 12), cursor="hand2")
    boton_menu.pack(side="right", padx=10, pady=5)

    # Adjuntar el menú a la ventana
    boton_menu.bind("<Button-1>", mostrar_menu)
    boton_menu.bind("<FocusOut>", restablecer_estado)
    

    label_session = tk.Label(frame_ver, text=email_activo, bg=color_fondo_principal, fg=color_texto_principal2, font=fuente_texto_principal2)
    label_session.pack(side="right", padx=(150, 10), pady=5)


    # Frame para los botones de "Crear"
    frame_crear = tk.Frame(ventana_principal, bg=color_fondo_principal)
    frame_crear.pack(anchor="w", padx=10, pady=5)

    label_crear = tk.Label(frame_crear, text="Crear", bg=color_fondo_principal, fg=color_texto_principal2, font=fuente_texto_principal2)
    label_crear.pack(side="left", padx=10, pady=5)

    boton_crear_producto = tk.Button(frame_crear, text="Crear Producto", command=ventana_crear_producto, bg=color_boton_principal, fg=color_texto_principal)
    boton_crear_producto.pack(side="left", padx=20, pady=5)

    boton_crear_almacen = tk.Button(frame_crear, text="Crear Almacén", command=ventana_crear_almacen, bg=color_boton_principal, fg=color_texto_principal)
    boton_crear_almacen.pack(side="left", padx=20, pady=5)
    
    if  (rol_activo == 1 or rol_activo == 3): 
     boton_crear_proveedor = tk.Button(frame_crear, text="Crear Proveedor", command=ventana_crear_proveedor, bg=color_boton_principal, fg=color_texto_principal)
     boton_crear_proveedor.pack(side="left", padx=20, pady=5)

     boton_crear_categoria = tk.Button(frame_crear, text="Crear Categoría", command=ventana_crear_categoria, bg=color_boton_principal, fg=color_texto_principal)
     boton_crear_categoria.pack(side="left", padx=20, pady=5)
    
    if  (rol_activo == 1 ): 
     boton_crear_usuario = tk.Button(frame_crear, text="Crear Usuario", command=ventana_crear_usuario, bg=color_boton_principal, fg=color_texto_principal)
     boton_crear_usuario.pack(side="left", padx=20, pady=5)

    # Frame para los botones de "Gráficos"
    frame_graficos = tk.Frame(ventana_principal, bg=color_fondo_principal)
    frame_graficos.pack(anchor="w", padx=10, pady=5)

    label_graficos = tk.Label(frame_graficos, text="Gráficos", bg=color_fondo_principal, fg=color_texto_principal2, font=fuente_texto_principal2)
    label_graficos.pack(side="left", padx=10, pady=5)

    boton_grafico_reportes = tk.Button(frame_graficos, text="Gráfico de Reportes", command=crear_ventanaGraficoReportes, bg=color_boton_principal, fg=color_texto_principal)
    boton_grafico_reportes.pack(side="left", padx=20, pady=5)

    boton_grafico_almacenes = tk.Button(frame_graficos, text="Gráfico de Almacenes", command=crear_ventanaGraficoAlmacenes, bg=color_boton_principal, fg=color_texto_principal)
    boton_grafico_almacenes.pack(side="left", padx=20, pady=5)

    boton_grafico_proveedores = tk.Button(frame_graficos, text="Gráfico de Proveedores", command=crear_ventana_grafico_proveedores, bg=color_boton_principal, fg=color_texto_principal)
    boton_grafico_proveedores.pack(side="left", padx=20, pady=5)

    boton_grafico_categorias = tk.Button(frame_graficos, text="Gráfico de Categorías", command=crear_ventanaGraficoCategorias, bg=color_boton_principal, fg=color_texto_principal)
    boton_grafico_categorias.pack(side="left", padx=20, pady=5)

    if  (rol_activo == 1 ):     
     boton_grafico_roles = tk.Button(frame_graficos, text="Gráfico de Roles", command=crear_ventana_grafico_roles, bg=color_boton_principal, fg=color_texto_principal)
     boton_grafico_roles.pack(side="left", padx=20, pady=5)


  
    # Mostrar la imagen
    imagen = Image.open("imagenLogo.jpg")
    imagen = imagen.resize((450, 450), resample=Image.LANCZOS)  
    imagen = ImageTk.PhotoImage(imagen)
    label_imagen = tk.Label(ventana_principal, image=imagen, bg=color_fondo_principal)
    label_imagen.place(relx=0.5, rely=0.6, anchor="center")

    

    # Ejecutar el bucle principal de la aplicación
    ventana_principal.mainloop()

def abrir_ventana_login():
    # Crear la ventana de inicio de sesión
    ventana_login = tk.Tk()
    ventana_login.title("Inicio de Sesión")
    ventana_login.geometry("700x400+500+250")
    ventana_login.resizable(False, False)  # Evitar que la ventana cambie de tamaño

    # Configuración de colores y estilos
    color_fondo = "#f0f0f0"
    color_texto = "#333333"
    fuente_texto = ("Arial", 12)
    color_boton = "DeepSkyBlue3"

    ventana_login.configure(bg=color_fondo)
    
    # Cargar la imagen
    imagen = Image.open("imagenLogo.jpg")
    imagen = imagen.resize((400, 400), resample=Image.LANCZOS)
    imagen = ImageTk.PhotoImage(imagen)

    # Mostrar la imagen en un Label
    label_imagen = tk.Label(ventana_login, image=imagen)
    label_imagen.pack(side="left", padx=10, pady=10)

    # Etiquetas y entradas para usuario y contraseña
    tk.Label(ventana_login, text="Usuario:", bg=color_fondo, fg=color_texto, font=fuente_texto).pack()
    entry_usuario = tk.Entry(ventana_login, bg=color_fondo, fg=color_texto, font=fuente_texto)
    entry_usuario.pack(pady=5)
    tk.Label(ventana_login, text="Contraseña:", bg=color_fondo, fg=color_texto, font=fuente_texto).pack()
    entry_contrasena = tk.Entry(ventana_login, show="*", bg=color_fondo, fg=color_texto, font=fuente_texto)
    entry_contrasena.pack(pady=5)
    # Función para verificar las credenciales de inicio de sesión
    def verificar_credenciales():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()

        my_database = my_client.Inventario
        my_collection = my_database.Usuario

        usuarioDB = []
        contrasenaDB = []
        rolDB = []


        campos = {
        "contraseña": 1,
        "email": 1,
        "id_rol":1,
        "_id": 0 
        }

        my_cursor = my_collection.find({ "email" : usuario}, campos )

        for item in my_cursor:
           usuarioDB.append(item['email'])
           contrasenaDB.append(item['contraseña'])
           rolDB.append(item['id_rol'])
           # Verificar credenciales 
           if usuario == usuarioDB[0] and contrasena == contrasenaDB[0]:
              rol_sesion = rolDB[0]
              email_sesion = usuarioDB[0]
              # Mostrar mensaje de éxito y abrir la ventana principal
              messagebox.showinfo("Inicio de sesión exitoso", "¡Bienvenido!")
              ventana_login.destroy()
              abrir_ventana_principal(rol_sesion, email_sesion)
           else:
              messagebox.showerror("Error de inicio de sesión", "Credenciales incorrectas")

    # Botón para iniciar sesión
    boton_iniciar_sesion = tk.Button(ventana_login, text="Iniciar Sesión", command=verificar_credenciales, bg=color_boton, fg="white", font=fuente_texto)
    boton_iniciar_sesion.pack(pady=10)

    ventana_login.mainloop()

abrir_ventana_login()