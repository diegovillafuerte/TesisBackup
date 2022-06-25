from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from database_setup import Base, Company, Applicant, Job, MatchScore
from sqlalchemy.orm import sessionmaker
import dbOperations
import locale
import os
import math
import googlemaps
import magic
import dbOperations
import pandas as pd
import numpy as np
from numpy.random import seed, rand, randn
import matplotlib.pyplot as plt
import scipy.stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import random
import string
from sklearn.metrics import classification_report


#engine = create_engine('postgres://localhost/simil')
db_user = os.environ['db_user']
db_pass = os.environ['db_pass']
db_host = os.environ['db_host']
db_port = os.environ['db_port']

engine = create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}?sslmode=require".format(db_user, db_pass, db_host, db_port, 'postgres'))

#engine = create_engine('postgres://localhost/simil')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Setup the api key for the api call
#apiKey = os.environ['GOOGLE_API_KEY']
#gmaps = googlemaps.Client(key=apiKey)

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
'''
for i in range(10):
	name="Auto Generado"
	mail="AutoGenerado_" + get_random_string(10)+"@gmail.com"
	print(mail)
	password=get_random_string(10)
	birthdate=str(random.randint(10,31)) + "/0" + str(random.randint(1,9)) + "/" + str(random.randint(1940,2005))
	print(birthdate)
	zipcode="11111"
	gender=str(random.randint(0,3))
	civil=str(random.randint(0,1))
	dependientes=str(random.randint(0,3))
	estudios=str(random.randint(0,5))
	responsePers={'p1': str(random.randint(1,5)), 'p2': str(random.randint(1,5)), 'p3': str(random.randint(1,5)), 'p4': str(random.randint(1,5)), 'p5': str(random.randint(1,5)), 'p6': str(random.randint(1,5)), 'p7': str(random.randint(1,5)), 'p8': str(random.randint(1,5)), 'p9': str(random.randint(1,5)), 'p10': str(random.randint(1,5)), 'p11': str(random.randint(1,5)), 'p12': str(random.randint(1,5)), 'p13': str(random.randint(1,5)), 'p14': str(random.randint(1,5)), 'p15': str(random.randint(1,5)), 'p16': str(random.randint(1,5)), 'p17': str(random.randint(1,5)), 'p18': str(random.randint(1,5)), 'p19': str(random.randint(1,5)), 'p20': str(random.randint(1,5)), 'submit': ''}
	responseMath={'p1': str(random.randint(1,5)), 'p2': str(random.randint(1,5)), 'p3': str(random.randint(1,5)), 'p4': str(random.randint(1,5)), 'p5': str(random.randint(1,5)), 'p6': str(random.randint(1,5)), 'p7': str(random.randint(1,5)), 'p8': str(random.randint(1,5)), 'p9': str(random.randint(1,5)), 'p10': str(random.randint(1,5)), 'submit': ''}


	dbOperations.createApplicant(name, mail, password)
	applicant_id = dbOperations.getApplicantID(mail)

	dbOperations.addDemoApplicant(birthdate, zipcode, gender, civil, dependientes, estudios, applicant_id)
	#input de addDemoApplicant 11/10/1993 11111 2 1  4 4

	dbOperations.addPersonality(responsePers, applicant_id)
	#input de personality {'p1': '2', 'p2': '3', 'p3': '4', 'p4': '2', 'p5': '3', 'p6': '4', 'p7': '2', 'p8': '3', 'p9': '2', 'p10': '3', 'p11': '4', 'p12': '3', 'p13': '2', 'p14': '3', 'p15': '3', 'p16': '2', 'p17': '3', 'p18': '2', 'p19': '3', 'p20': '4', 'submit': ''} 4

	dbOperations.addMath(responseMath, applicant_id)
	#input de addMath {'p1': '3', 'p2': '5', 'p3': '5', 'p4': '2', 'p5': '3', 'p6': '4', 'p7': '2', 'p8': '3', 'p9': '1', 'p10': '1', 'submit': ''} 4
'''

#magic.generaModeloNevo(1)

#charVector = magic.getCharacteristicVector(1, 4, 1)

#Generar base con 1000 observaciones (mitad verdad mitad)
#magic.simulateDB(charVector, 5000, .5)

#magic.entrenarModeloLog(open("base.csv", mode='r'))

#score = magic.matchScore(job_id, applicant_id)
#print(score)
'''
trabajo = session.query(Job).filter(Job.id == 2).one()
# 1 | lala                            |    123 | iuifr        |        3 | t      | {{34225,108080,11,10,2,11}} | {{56,50,50,50,75}} | {{1}}  | 09098   | {7.727850156878312e-05,-0.004529094138303391,0.8580003868697113,-0.3469685989177618,0.1616235053105845,-1.1108586077409077,0.5379376230665155,0.3112350287071894,0.5285773936673395,0.33421910695629403,0.8347837488313626,0.012286866865584473} | 0.9282632084229319 |          1
  2 | de                              |    432 | dde          |        1 | t      | {{33860,101010,11,10,1,14}} | {{56,56,56,56,43}} | {{2}}  | 05348   | {2.727850156878312e-05,-0.004529094138303391,0.8580003868697113,-0.3469685989177618,0.1616235053105845,1.1108586077409077,1.5379376230665156,-1.3112350287071894,2.5285773936673395,0.33421910695629403,1.8347837488313625,6.012286866865584}    |     0.601823740172 |          1
trabajo.coeficientes = [2.727850156878312e-05, -0.004529094138303391, 0.8580003868697113, -0.3469685989177618, 0.1616235053105845, 1.1108586077409077, 1.5379376230665155, -1.3112350287071894, 2.5285773936673395, 0.33421910695629403, 1.8347837488313626, 6.012286866865584473]
session.commit()'''

'''
applicants = session.query(Applicant).all()
for app in applicants:
	id1 = app.id
	print("El score entre " + app.mail + " y la empresa 2 es: ")
	print(magic.matchScore(2, id1))
	print("")'''



'''
#Autogenerar trabajos para una empresa dada 
for i in range(5):
	title="Trabajo Auto Generado" + get_random_string(10)
	salary = str(random.randint(100,50000))
	description = "Buen trabajo"
	company_id = 1
	openings = 1
	status = 1
	zipcode = 11111
	#mail="TrabajoAutoGenerado_" + get_random_string(10)+"@gmail.com"
	#password=get_random_string(10)
	birthdate=str(random.randint(10,31)) + "/0" + str(random.randint(1,9)) + "/" + str(random.randint(1940,2005))
	zipcode="11111"
	gender=str(random.randint(0,3))
	civil=str(random.randint(0,1))
	dependientes=str(random.randint(0,3))
	estudios=str(random.randint(0,5))
	responsePers={'p1': str(random.randint(1,5)), 'p2': str(random.randint(1,5)), 'p3': str(random.randint(1,5)), 'p4': str(random.randint(1,5)), 'p5': str(random.randint(1,5)), 'p6': str(random.randint(1,5)), 'p7': str(random.randint(1,5)), 'p8': str(random.randint(1,5)), 'p9': str(random.randint(1,5)), 'p10': str(random.randint(1,5)), 'p11': str(random.randint(1,5)), 'p12': str(random.randint(1,5)), 'p13': str(random.randint(1,5)), 'p14': str(random.randint(1,5)), 'p15': str(random.randint(1,5)), 'p16': str(random.randint(1,5)), 'p17': str(random.randint(1,5)), 'p18': str(random.randint(1,5)), 'p19': str(random.randint(1,5)), 'p20': str(random.randint(1,5)), 'submit': ''}
	responseMath={'p1': str(random.randint(1,5)), 'p2': str(random.randint(1,5)), 'p3': str(random.randint(1,5)), 'p4': str(random.randint(1,5)), 'p5': str(random.randint(1,5)), 'p6': str(random.randint(1,5)), 'p7': str(random.randint(1,5)), 'p8': str(random.randint(1,5)), 'p9': str(random.randint(1,5)), 'p10': str(random.randint(1,5)), 'submit': ''}


	dbOperations.createJob(title, salary, description, company_id, openings, status, zipcode)
	job_id = session.query(Job).filter(Job.company_id == company_id, Job.title == title).one().id

	dbOperations.addDemoJob(birthdate, zipcode, gender, civil, dependientes, estudios, company_id, job_id)
	#input de addDemoApplicant 11/10/1993 11111 2 1  4 4

	dbOperations.addPersonalityJob(responsePers, company_id, job_id)
	#input de personality {'p1': '2', 'p2': '3', 'p3': '4', 'p4': '2', 'p5': '3', 'p6': '4', 'p7': '2', 'p8': '3', 'p9': '2', 'p10': '3', 'p11': '4', 'p12': '3', 'p13': '2', 'p14': '3', 'p15': '3', 'p16': '2', 'p17': '3', 'p18': '2', 'p19': '3', 'p20': '4', 'submit': ''} 4

	dbOperations.addMathJob(responseMath, job_id)
	#input de addMath {'p1': '3', 'p2': '5', 'p3': '5', 'p4': '2', 'p5': '3', 'p6': '4', 'p7': '2', 'p8': '3', 'p9': '1', 'p10': '1', 'submit': ''} 4
'''

trabajos="Cajero Sr. ,Cajero,Asistente ejecutivo,Gerente de planta,Asociado de piso,Telefonista,Chofer,Encargado de seguridad,Programador,Abogado asistente,Director General,Gerente de marca,Especialista de ensamblado,Obrero,Especialista de limpieza,Analista de riesgo,Analista de negocios,Analista de ventas,Director de estrategia comercial,Gerente de tienda,Encargado de sección".split(",")
empresas=["PromoTec","COMSA"]
descripciones= "Actuar de punto de contacto administrativo entre los ejecutivos y los clientes internos y externos/Estará a cargo de procesar, registrar y administrar todas las transacciones financieras que se llevan a cabo en el negocio. Los cajeros son responsables de la recepción del pago y de su correcta administración, por lo que deben estar bien capacitados para desempeñar bien sus labores./Trabajar en estrecho contacto con los clientes para determinar sus necesidades, responder a sus preguntas sobre los productos y recomendar las soluciones adecuadas./Informar sobre los servicios que ofrecemos, captar el cliente, supervisar y mantener el buen estado del local/Manejar y conducir el vehículo asignado a la Dirección así como apoyar en las actividades que se desempeñan en la misma./Coordina el funcionamiento de los/las vigilantes y los sistemas de seguridad de la empresa de seguridad. Organiza, dirige e inspecciona al personal de seguridad privada. Propone los sistemas de seguridad más adecuados en cada caso, supervisa su uso, el funcionamiento y la conservación o mantenimiento./Responsable del desarrollo de programas que ayuden a automatizar y sistematizar procesos operativos y administrativos que se necesiten./Atención, orientación y asesoría legal a personas con alguna controversia familiar, laboral, civil o penal. Elaboración de demandas, contestaciones y escritos en general de índole legal./coordinar todas las actividades de una empresa u organización, es decir, supervisan el desempeño de los empleados, controlan los presupuestos, establecen los objetivos generales, además de asegurar que todas estas actividades se realicen de manera eficiente, organizada y segura/Será el responsable del desarrollo y ejecución de planes de mercadeo de las marcas asignadas, deberá hacer la promoción de estas líneas con médicos, hospitales e instituciones. Deberá crear y diseñar estrategias de promoción e incrementar las ventas, llevar el presupuesto de ventas y promociones./Lectura y comprensión de instrucciones y seguimiento de los procedimientos establecidos. Recopilación de todos los equipos y materiales necesarios para comenzar el proceso. Toma de mediciones de precisión para asegurar el perfecto encaje de los componentes.".split("/")
todos = session.query(MatchScore).all()	
for match in todos:
	match.scores = random.randint(65,100)
session.commit()

	



