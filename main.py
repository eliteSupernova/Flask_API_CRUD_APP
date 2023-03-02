import pymysql
from app import app
from flaskext.mysql import MySQL
from flask import Flask,request,jsonify

app=Flask(__name__)

mysql=MySQL()
app.config['MYSQL_DATABASE_USER']="root"
app.config['MYSQL_DATABASE_PASSWORD']="password"
app.config['MYSQL_DATABASE_DB']="employee"
app.config['MYSQL_DATABASE_HOST']="localhost"
mysql.init_app(app)


@app.route("/emp",methods=['GET'])
def emp():
    conn=mysql.connect()
    cur=conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM emp;")
    rows=cur.fetchall()
    resp=jsonify(rows)
    return resp


@app.route('/create', methods=['POST'])
def create():
    try:
        _json = request.json
        _ID = _json['ID']
        _EMP_ID = _json['EMP_ID']
        _EMP_NAME = _json['EMP_NAME']
        _DESIG = _json['DESIG']
        _SAL = _json['SAL']
        if _ID and _EMP_ID and _EMP_NAME and _DESIG and _SAL and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery= "INSERT INTO EMP(ID,EMP_ID,EMP_NAME,DESIG,SAL) VALUES(%s,%s,%s,%s,%s);"
            bindData=(_ID,_EMP_ID,_EMP_NAME,_DESIG,_SAL)
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            resp = jsonify("employee added successfully")
            return resp
        else:
            return "Failed"
    except Exception as e:
        return jsonify({"Message":str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route("/emp/read/<int:EMP_ID>", methods=['GET'])
def read(EMP_ID):
    try:
        if request.method=="GET":
            conn=mysql.connect()
            cursor=conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM EMP WHERE EMP_ID=%s",EMP_ID)
            emp = cursor.fetchone()
            resp = jsonify(emp)
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route("/emp/delete/<int:EMP_ID>", methods=['DELETE'])
def delete(EMP_ID):
    try:
        if request.method=="DELETE":
            conn=mysql.connect()
            cursor=conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("DELETE FROM EMP WHERE EMP_ID=%s",EMP_ID)
            conn.commit()
            resp = jsonify("DELETE SUCCESSFULLY!")
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route("/emp/update/<int:EMP_ID>", methods=['PUT'])
def update(EMP_ID):
    try:
        _json = request.json
        _ID = _json['ID']
        _EMP_ID = _json['EMP_ID']
        _EMP_NAME = _json['EMP_NAME']
        _DESIG = _json['DESIG']
        _SAL = _json['SAL']
        if _ID and _EMP_ID and _EMP_NAME and _DESIG and _SAL and request.method == 'PUT':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE EMP SET ID=%s,EMP_NAME=%s,DESIG=%s,SAL=%s WHERE EMP_ID=%s;"
            bindData = (_ID,_EMP_NAME, _DESIG, _SAL,EMP_ID)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            resp = jsonify("MPLOYEE UPDATED SUCCESSFUL")
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()



if __name__=="__main__":
    app.run(host='0.0.0.0' ,port=5002,debug = True)