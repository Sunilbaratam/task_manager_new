from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///prod.db'
db=SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200),nullable=False)
    id_created_at = db.Column(db.DateTime, default = datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' :
        task_text = request.form['message']
        new_task = Task(message = task_text)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Add the task properly"
    else:
        tasks = Task.query.order_by(Task.id_created_at).all()
        return render_template('index.html', tasks=tasks)



@app.route('/delete/<int:id>')
def delete(id):
    task_d = Task.query.get_or_404(id)

    try:
        db.session.delete(task_d)
        db.session.commit()
        return redirect('/')
    except:
        return 'Delete the task properly'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_u = Task.query.get_or_404(id)
    
    if request.method == 'POST':
        task_u.message = request.form['message']
        task_u.id_created_at = datetime.utcnow()

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return 'Update the task properly'

    else:
        return render_template('update.html', task=task_u)
    
if __name__ == "__main__":
    app.run(debug = True)
    

