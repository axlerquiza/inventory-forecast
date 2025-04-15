from flask import g, request
from flask_login import login_required, current_user
from datetime import datetime, timezone
from models.notification import Notification
from . import notifications_bp

@notifications_bp.before_app_request
def load_recent_notifications():
    """Load recent notifications and calculate time since for each."""
    # Skip loading notifications for unauthenticated users or during logout
    if not current_user.is_authenticated or (request.endpoint and request.endpoint == 'auth.logout'):
        g.recent_notifications = []
        return

    notifications = Notification.query.order_by(Notification.timestamp.desc()).limit(10).all()
    # Add a 'time_since' attribute to each notification
    for notification in notifications:
        notification.time_since = calculate_time_since(notification.timestamp)
    g.recent_notifications = notifications

def calculate_time_since(timestamp):
    """Calculate the time difference between now and the given timestamp."""
    if timestamp.tzinfo is None:
        # Make the timestamp timezone-aware if it is naive
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)  # Use timezone from datetime module
    diff = now - timestamp

    if diff.days >= 365:
        return f"{diff.days // 365}y"
    elif diff.days >= 30:
        return f"{diff.days // 30}m"
    elif diff.days >= 7:
        return f"{diff.days // 7}w"
    elif diff.days >= 1:
        return f"{diff.days}d"
    elif diff.seconds >= 3600:
        return f"{diff.seconds // 3600}h"
    elif diff.seconds >= 60:
        return f"{diff.seconds // 60}m"
    else:
        return f"{diff.seconds}s"
