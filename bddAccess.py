# -*- coding: UTF-8 -*-

'''
Created on 21 feb. 2014

@author: Olivia Gautrais
'''

import MySQLdb, os
import bddExceptions as exceptions

here = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(here,"bddCredentials.txt"),"r")

f.close()

def ouvrirConnexion():
    """
    Connexion à une base de données
    """
    conn = MySQLdb.connect(host = "Efferalgan.mysql.pythonanywhere-services.com", user = "Efferalgan", passwd = "motdepassetoutnul", db = "Efferalgan$default", charset="utf8", use_unicode=True)
    # création d'un curseur pour accéder à cette base
    cur = conn.cursor()

    cur.execute('SET NAMES utf8mb4')
    cur.execute("SET CHARACTER SET utf8mb4")
    cur.execute("SET character_set_connection=utf8mb4")

    return (cur, conn)

def executerReq(cur, req, variables=None):
    """
    Requête à la base de données
    """
    cur.execute(req, variables)

def validerModifs(conn):
    conn.commit()


def fermerConnexion(cur, conn):
    """
    Fermeture de la connexion
    """
    cur.close()
    conn.close()