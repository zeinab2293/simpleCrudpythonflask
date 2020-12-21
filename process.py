import pymysql
from flask import Flask, render_template, request, jsonify

from db_config import mysql
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('form.html')
 #Add
@app.route('/process', methods=['POST'])
def add():

	email = request.form['email']
	name = request.form['name']

	if name and email :
		newName = name 
		sql = "INSERT INTO tbl_user(user_name, user_email) VALUES(%s, %s)"
		data = (name ,email)
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(sql, data)
		conn.commit()
		resp = jsonify('User added successfully!')
		resp.status_code = 200
		return jsonify({'name' : newName})
	return jsonify({'error' : 'Missing data!'})
# Get All Users

@app.route('/users')

def users():

	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_user")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

		#Get 1 user 
@app.route('/user/<int:id>')
def user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_user WHERE user_id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		#Update User 
@app.route('/update', methods=['POST'])
def update_user():
	try:
		_json = request.json
		_id = _json['id']
		_name = _json['name']
		_email = _json['email']
			
		# validate the received values
		if _name and _email  and _id and request.method == 'POST':
			
			# save edits
			sql = "UPDATE tbl_user SET user_name=%s, user_email=%s WHERE user_id=%s"
			data = (_name, _email, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		# Delete User 
@app.route('/delete/<int:id>')
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
		conn.commit()
		resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
	


if __name__ == '__main__':
	app.run(debug=True)