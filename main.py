from flask import *
from SQLiteQueries import SQLiteData
from datetime import datetime

app = Flask(__name__)


def date_display(date):
    date_format = "%Y-%m-%d %H:%M:%S"
    date_obj = datetime.strptime(date, date_format)
    return date_obj.strftime("%d/%m/%Y %H:%M")


@app.route('/')
def home():
    db = SQLiteData('Task_Data')
    Records = db.read()
    args = request.args
    record = None
    if args.get('uid'):
        record = db.read([('ID', '=', int(args.get('uid')))])
    return render_template("new.html", records=Records, date_display=date_display, record=record and record[0])


@app.route('/add', methods=['POST'])
def add():
    args = request.form
    data = {
        'TASK': args.get('task'),
        'TASK_DESC': args.get('task_desc'),
        'ISDONE': False
    }
    db = SQLiteData('Task_Data')
    db.create(data)
    return redirect("/")


@app.route('/delete')
def delete():
    record_id = request.args.get('id')
    if record_id:
        db = SQLiteData('Task_Data')
        db.delete([('ID', '=', record_id)])
    return redirect("/")


@app.route('/complete')
def complete():
    record_id = request.args.get('id')
    data_to_update = {'ISDONE': True}
    con = [('ID', '=', record_id)]
    db = SQLiteData('Task_Data')
    db.update(data_to_update, con)
    return redirect("/")


@app.route('/reopen')
def reopen():
    record_id = request.args.get('id')
    data_to_update = {'ISDONE': False}
    con = [('ID', '=', record_id)]
    db = SQLiteData('Task_Data')
    db.update(data_to_update, con)
    return redirect("/")


@app.route('/update', methods=['POST'])
def update():
    args = request.form
    data_to_update = {'TASK': args.get('task'), 'TASK_DESC': args.get('task_desc')}
    con = [('ID', '=', args.get('id'))]
    db = SQLiteData('Task_Data')
    db.update(data_to_update, con)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
