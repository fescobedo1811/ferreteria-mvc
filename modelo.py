import sqlite3
import re
from tkinter import messagebox, END
from tkinter import *


# ##############################################
# MODELO
# ##############################################
# 
def conexion():
    con = sqlite3.connect("ferreteria.db")
    return con


def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS ventas
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto varchar(20),
            cantidad int,
            precio_unit float,
            precio_total float,
            forma_pago varchar(20),
            tipo_cliente varchar(20))
            """
         
    cursor.execute(sql)
    con.commit()


try:
    conexion()
    crear_tabla()
except:
    print("Error en la tabla")




def agregar(producto, cantidad, precio_unit, precio_total, forma_pago, tipo_cliente, tree):
    con = conexion()
    cursor = con.cursor()
    data = (producto, cantidad, precio_unit, precio_total, forma_pago, tipo_cliente)
    sql = "INSERT INTO ventas(producto, cantidad, precio_unit, precio_total, forma_pago, tipo_cliente) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    con.commit()
    messagebox.showinfo("Venta", "Venta registrada")
    actualizar_treeview(tree)
#    limpiar()
    producto.set("")
    cantidad.set("")
    precio_unit.set("")
    precio_total.set("")


def borrar(tree):
    confirma = messagebox.askquestion("ADVERTENCIA", "¿Está seguro qué desea borrar el registro?")
    if confirma == 'no':
        return

    valor = tree.selection()
    item = tree.item(valor)
    id = item['text']

    con = conexion()
    cursor = con.cursor()
    data = (id,)
    sql = "DELETE FROM ventas WHERE id = ?"
    cursor.execute(sql, data)
    con.commit()
    tree.delete(valor)
    messagebox.showinfo("Venta", "Registro borrado")


def actualizar_treeview(tree):
    records = tree.get_children()
    for element in records:
        tree.delete(element)

    sql = "SELECT * FROM ventas ORDER BY id ASC"
    con = conexion()
    cursor = con.cursor()
    datos = cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        print(fila)
        tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]))


def update(id, producto, cantidad, precio_unit, precio_total, forma_pago, tipo_cliente, tree):
    if not id:
        messagebox.showinfo("MODIFICAR", "Debe escribir un ID válido para modificar.")
        return

    con = conexion()
    cursor = con.cursor()
    data = (producto, cantidad, precio_unit, precio_total, forma_pago, tipo_cliente, id)
    sql = "UPDATE ventas SET producto=?, cantidad=?, precio_unit=?, precio_total=?, forma_pago=?, tipo_cliente=? WHERE id=?;"
    cursor.execute(sql, data)
    con.commit()
    con.close()
    messagebox.showinfo("Información", "Venta modificada")
    actualizar_treeview(tree)
 #   limpiar()


#def limpiar():
#    producto.set("")
#    cantidad.set("")
#    precio_unit.set("")
#    precio_total.set("") 
#    modificar.set("")
    #entry_forma_pago.delete(0, END)
    #entry_tipo_cliente.delete(0, END)

#LA FUNCION CARGAR_DATOS FUNCIONA COMO CONSULTA
# YA QUE SE UTILIZA PARA CARGAR LOS DATOS EXISTENTES
# EN LA BASE DE DATOS
def cargar_datos(tree):
    for item in tree.get_children():
        tree.delete(item)
        
    con = conexion()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM ventas ORDER BY id DESC")
    rows = cursor.fetchall()
    
    for row in rows:
        tree.insert("", END, text=row[0], values=row[1:])
    con.close()