from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-me-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helpdesk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Simple admin password
# Prefer setting via environment variable: ADMIN_PASSWORD
# Fallback set as requested
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Dlc7330')

db = SQLAlchemy(app)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='Medium')
    status = db.Column(db.String(20), default='Open')
    remote_requested = db.Column(db.Boolean, default=False)
    remote_details = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    comments = db.relationship('Comment', backref='ticket', lazy=True, cascade='all, delete-orphan')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            flash('Please log in as admin to access this.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin'] = True
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        flash('Invalid password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash('Logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/')
def index():
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return render_template('index.html', tickets=tickets, is_admin=session.get('admin'))

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        ticket = Ticket(
            name=request.form['name'],
            email=request.form['email'],
            subject=request.form['subject'],
            description=request.form['description'],
            priority=request.form.get('priority', 'Medium'),
            remote_requested='remote' in request.form
        )
        db.session.add(ticket)
        db.session.commit()
        flash(f'Ticket submitted successfully! Your ticket ID is #{ticket.id}', 'success')
        return redirect(url_for('ticket', ticket_id=ticket.id))
    return render_template('submit.html')

@app.route('/ticket/<int:ticket_id>')
def ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template('ticket.html', ticket=ticket, is_admin=session.get('admin'))

@app.route('/ticket/<int:ticket_id>/update', methods=['POST'])
@admin_required
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.status = request.form.get('status', ticket.status)
    ticket.remote_details = request.form.get('remote_details', ticket.remote_details)
    db.session.commit()
    flash('Ticket updated.', 'success')
    return redirect(url_for('ticket', ticket_id=ticket_id))

@app.route('/ticket/<int:ticket_id>/comment', methods=['POST'])
def add_comment(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    comment = Comment(
        ticket_id=ticket_id,
        author=request.form['author'],
        content=request.form['content']
    )
    db.session.add(comment)
    db.session.commit()
    flash('Comment added.', 'success')
    return redirect(url_for('ticket', ticket_id=ticket_id))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
