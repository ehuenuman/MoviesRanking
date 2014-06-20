#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3


def conectar():
    """Funcion que conecta la base de datos
    y retorna el conector
    @return con"""
    con = sqlite3.connect('movies.db')
    con.row_factory = sqlite3.Row
    return con


def obtener_movies():
    """Funcion que retorna la informacion de la tabla movies
    @return productos"""
    con = conectar()
    c = con.cursor()
    query = "SELECT * FROM movies"
    resultado = c.execute(query)
    movies = resultado.fetchall()
    con.close()
    return movies


def infoFila(codigo):
    """Funcion que retorna la informacion de una fila
    @return valores"""
    con = conectar()
    c = con.cursor()
    query = "SELECT * FROM movies WHERE id=?"
    resultado = c.execute(query, [codigo])
    infoFila = resultado.fetchall()
    con.close()
    for row in infoFila:
        valores = [row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]
    return valores


def subir(iD,valores):
    """Funcion que edita un valor en la
    base de datos y retorna una variable
    booleana
    @param codigo,valores
    @return exito"""
    exito = False
    con = conectar()
    c = con.cursor()
#    iD = valores[0]
    ti = valores[0]
    po = valores[1]
    year = valores[2]
    dirc = valores[3]
    coun = valores[4]
    star = valores[5]
    des = valores[6]
    ran = iD
    total = (ti, po, year, dirc, coun, star, des, ran, iD)
    query = '''UPDATE movies
            SET title=?,poster=?,release_year=?, director=?,country=?, stars=?, description=?, ranking=?
            WHERE iD=? '''
    try:
        c.execute(query, total)
        con.commit()
    except sqlite3.Error as e:
        print "Error:",e.arg[0]
    con.close()

if __name__ == '__main__':
    print "hola"