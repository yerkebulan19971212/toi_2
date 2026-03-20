"""
Email notifications for invitation events.
Sent in a background thread to avoid blocking the HTTP response.
"""
import threading

from django.conf import settings
from django.core.mail import send_mail


def _send(subject, body, to_email):
    """Fire-and-forget email in a daemon thread."""
    if not to_email:
        return

    def _do_send():
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                fail_silently=True,
            )
        except Exception:
            pass  # Never crash the request

    t = threading.Thread(target=_do_send, daemon=True)
    t.start()


def notify_rsvp(invitation, rsvp):
    """Notify invitation owner about a new RSVP response."""
    owner = invitation.owner
    if not owner or not owner.email:
        return

    choice_labels = {
        'solo': 'Иә, жалғыз өзім барамын',
        'with_partner': 'Жұбайыммен бірге барамын',
        'declined': 'Өкінішке орай, келе алмаймын',
    }
    choice_text = choice_labels.get(rsvp.response, rsvp.response)
    title = invitation.get_display_title()

    subject = f'Жаңа RSVP жауабы — {title}'
    body = (
        f'Сіздің "{title}" шақыруыңызға жаңа жауап келді.\n\n'
        f'Қонақ: {rsvp.guest_name}\n'
        f'Телефон: {rsvp.phone or "—"}\n'
        f'Жауабы: {choice_text}\n\n'
        f'Барлық жауаптарды қарау үшін жеке кабинетіңізге кіріңіз.'
    )
    _send(subject, body, owner.email)


def notify_comment(invitation, comment):
    """Notify invitation owner about a new guest comment."""
    owner = invitation.owner
    if not owner or not owner.email:
        return

    title = invitation.get_display_title()
    subject = f'Жаңа пікір — {title}'
    body = (
        f'Сіздің "{title}" шақыруыңызға жаңа пікір жазылды.\n\n'
        f'Қонақ: {comment.guest_name}\n'
        f'Пікір: {comment.comment}\n\n'
        f'Барлық пікірлерді қарау үшін жеке кабинетіңізге кіріңіз.'
    )
    _send(subject, body, owner.email)
