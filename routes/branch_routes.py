# Branch management routes
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from models.models import Branch

branch_bp = Blueprint('branch', __name__, url_prefix='/branches', template_folder='../templates')

@branch_bp.route('/')
@login_required
def list_branches():
    branches = Branch.query.order_by(Branch.name).all()
    return render_template('branches.html', branches=branches)

@branch_bp.route('/create', methods=['POST'])
@login_required
def create_branch():
    name = request.form.get('name')
    location = request.form.get('location')
    if Branch.query.filter_by(name=name).first():
        flash('Branch with that name exists', 'warning')
        return redirect(url_for('branch.list_branches'))
    b = Branch(name=name, location=location)
    db.session.add(b)
    db.session.commit()
    flash('Branch created', 'success')
    return redirect(url_for('branch.list_branches'))

@branch_bp.route('/delete/<int:branch_id>', methods=['POST'])
@login_required
def delete_branch(branch_id):
    b = Branch.query.get_or_404(branch_id)
    db.session.delete(b)
    db.session.commit()
    flash('Branch deleted', 'info')
    return redirect(url_for('branch.list_branches'))
