import flask
from flask import Flask, request, jsonify, render_template
from flask import Response
import mysql.connector
import datetime

app = Flask(__name__)

app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return render_template('solus.html')


@app.route('/api/products', methods=['GET'])
def getProducts():
    #cursor=connectTodDB()
    mydb = mysql.connector.connect(
      host="localhost",
      port="8889",
      user="root",
      password="root",
      database="flask"
    )
    cursor = mydb.cursor()
    sql="SELECT codePrestation, prestation FROM Prestation"
    cursor.execute(sql)
    results = cursor.fetchall()
    row_headers=[x[0] for x in cursor.description] #get headers
    cursor.close()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)

@app.route('/api/product', methods=['GET'])
def getProduct():
    #cursor=connectTodDB()
    mydb = mysql.connector.connect(
      host="localhost",
      port="8889",
      user="root",
      password="root",
      database="flask"
    )

    if 'codePrestation' in request.args:
        codePrestation = request.args['codePrestation']
    else:
        return "Error: No codePrestation provided. Please specify a codePrestation."

    cursor = mydb.cursor()
    sql="SELECT codePrestation, prestation, prix FROM Prestation where codePrestation="+codePrestation
    cursor.execute(sql)
    results = cursor.fetchall()
    row_headers=[x[0] for x in cursor.description] #get headers
    cursor.close()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)

@app.route('/api/client', methods=['GET'])
def getClient():
    #cursor=connectTodDB()
    mydb = mysql.connector.connect(
      host="localhost",
      port="8889",
      user="root",
      password="root",
      database="flask"
    )

    if 'codeClient' in request.args:
        codeClient = request.args['codeClient']
    else:
        return "Error: No codeClient provided. Please specify a codeClient."

    cursor = mydb.cursor()
    sql="SELECT codeClient, civilite, nom, prenom, adresse, codePostal, ville, Carte.carte, remise FROM Client, Carte where codeClient="+codeClient+" and Client.carte=Carte.codeCarte"
    cursor.execute(sql)
    results = cursor.fetchall()
    row_headers=[x[0] for x in cursor.description] #get headers
    cursor.close()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)



@app.route('/api/order', methods=['POST'])
def newOrder():
    mydb = mysql.connector.connect(
      host="localhost",
      port="8889",
      user="root",
      password="root",
      database="flask"
    )
    cursor = mydb.cursor()
    orderDate= datetime.datetime.now()
    total=request.form['total']
    codeClient=request.form["codeClient"]
    sql="insert into Commande (prixTotal,dateCommande,codeClient) values ("+total+",'"+str(orderDate)+"',"+codeClient+")"
    cursor.execute(sql)
    mydb.commit()

    sql="select numCommande from Commande where codeClient='"+codeClient+"' and dateCommande='"+str(orderDate)+"'"
    cursor.execute(sql)
    result = cursor.fetchone()
    numCommande=result[0]

    for i in range(1,int(request.form["nbProduits"])+1):
        codePrestation=request.form["codePrestation"+str(i)]
        qte=request.form["qte"+str(i)]
        sql="insert into Ligne values ("+str(numCommande)+","+codePrestation+","+str(qte)+")"
        cursor.execute(sql)
        mydb.commit()
    cursor.close()
    return "order saved."



app.run()