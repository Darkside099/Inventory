# Alerts management and resolving
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from models.models import Alert

alert_bp = Blueprint('alerts', __name__, url_prefix='/alerts', template_folder='../templates')

@alert_bp.route('/')
@login_required
def list_alerts():
    alerts = Alert.query.order_by(Alert.created_at.desc()).all()
    return render_template('alerts.html', alerts=alerts)

@alert_bp.route('/resolve/<int:alert_id>', methods=['POST'])
@login_required
def resolve_alert(alert_id):
    a = Alert.query.get_or_404(alert_id)
    a.resolved = True
    db.session.commit()
    flash('Alert resolved', 'success')
    return redirect(url_for('alerts.list_alerts'))
