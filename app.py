from flask import Flask, render_template, request, redirect, url_for
from models import db # importamos el modulo db que contiene las funciones de conexion a la base de datos

app = Flask(__name__) # inicializamos la aplicacion flask

@app.route('/')
def index():
    conn = db.get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM tasks') # ejecutamos la consulta para obtener todas las tareas de la base de datos
    tasks = c.fetchall() # obtenemos todas las tareas de la base de datos
    conn.close() # cerramos la conexion a la base de datos
    return render_template('index.html', tasks=tasks)

# Primer endpoint para agregar una tarea
@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    prioridad = request.form.get('priority')
    fecha = request.form.get('date') 
    # obtenemos los datos del formulario, si no se envian, se guardan como None

    if task and prioridad and fecha:
        conn = db.get_db_connection()
        c = conn.cursor()
        c.execute('INSERT INTO tasks (text, priority, date, done) VALUES (?, ?, ?, ?)', (task, prioridad, fecha, 0))  # insertamos la tarea en la base de datos
        conn.commit()  # confirmamos los cambios
        conn.close()  # cerramos la conexion a la base de datos
    return redirect(url_for('index'))  # redirigimos a la pagina principal

# Segundo endpoint para completar una tarea
@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    conn = db.get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE tasks SET done = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


# Tercer endpoint para eliminar una tarea
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    conn = db.get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.init_db()  # inicializamos la base de datos al iniciar la aplicacion, antes de iniciar el servidor
    app.run(debug=True, port=5000)  # iniciamos la aplicacion en modo debug y en el puerto 5000

