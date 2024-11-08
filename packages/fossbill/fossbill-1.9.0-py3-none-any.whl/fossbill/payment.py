import stripe
import functools
from flask import (
    Blueprint, flash, g, current_app, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from fossbill.auth import login_required
from fossbill.database import get_db
from fossbill.auth import load_logged_in_user, get_system_smtp_server
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert, select, join
import datetime
from flask_weasyprint import render_pdf, HTML
import smtplib
from email.message import EmailMessage

bp = Blueprint('payment', __name__, url_prefix='/payments')

def get_stripe():
    if 'stripe' not in g:
        g.stripe = stripe
        g.stripe.set_app_info(
            'fossbill/willow-production',
            version='1.0.0',
            url='https://fossbill.org'
        )

        g.stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')

    return stripe

def payment_enabled(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not current_app.config.get('PAYMENT_ENABLED'):
            return redirect(url_for('landing.home'))

        return view(**kwargs)

    return wrapped_view

def user_charged(user):
    if not user.due_at:
        return False

    return datetime.date.today() <= user.due_at

def grace_days():
    grace_days = 7
    if current_app.config.get('GRACE_PERIOD_DAYS'):
        grace_days = current_app.config.get('GRACE_PERIOD_DAYS')

    return grace_days

def user_grace_period(user):
    if user_charged(user):
        return False

    return datetime.date.today() <= user.created_at + datetime.timedelta(days=grace_days())

def user_subscription_valid(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user.admin and not g.user.free and not (user_charged(g.user) or user_grace_period(g.user)):
            return redirect(url_for('payment.index'))

        return view(**kwargs)

    return wrapped_view

def send_charged_user_notice(payment, user_pref):
    body = render_template(
        'payment/charged_notice.plain',
        payment=payment,
    )

    msg = EmailMessage()
    msg["From"] = current_app.config['SMTP_USERNAME']
    msg["To"] = user_pref.email
    msg["Subject"] = "Fossbill - Payment notice"
    msg.set_content(body)

    server = get_system_smtp_server()
    server.send_message(msg)
    server.quit()

def charge_user(user, user_pref):
    if (user_charged(user) or user_grace_period(user)):
        return

    stripe = get_stripe()

    charge = stripe.Charge.create(
        amount=10 * 100,
        currency="eur",
        customer=user.stripe_customer,
        description="Fossbill.org subscription monthly payment"
    )

    engine, metadata = get_db()
    payments = metadata.tables['payment']

    with engine.connect() as conn:
        stmt = metadata.tables['user'].update().values(
            due_at=datetime.date.today() + datetime.timedelta(days=30)
        ).where(
            metadata.tables['user'].c.id == user.id,
        )
        result = conn.execute(stmt)

        stmt = insert(payments).values(
            user_id=user.id,
            payload=charge,
            date=datetime.date.today(),
            valid_for_service_thru=datetime.date.today() + datetime.timedelta(days=30),
            amount=charge['amount'],
            currency=charge['currency'],
            card_brand=charge['payment_method_details']['card']['brand'].capitalize(),
            card_last4=charge['payment_method_details']['card']['last4'],
            receipt_url=charge['receipt_url'],
        )
        result = conn.execute(stmt)

        conn.commit()

        stmt = select(payments).where(
            payments.c.id == result.inserted_primary_key[0]
        )
        result = conn.execute(stmt)

        if user_pref.email:
            send_charged_user_notice(result.fetchone(), user_pref)

@bp.route('/')
@login_required
@payment_enabled
def index():
    if user_charged(g.user):
        flash(_('Subscription active and expire the {}').format(g.user.due_at))
    elif user_grace_period(g.user):
        flash(_('Grace period on. Register a payment method.'), 'warning')
    elif g.user.admin:
        flash(_('You are admin, but you can still pay for the service.'), 'warning')
    elif g.user.free:
        flash(_('Free mode on, but you can still pay for the service.'), 'warning')
    else:
        flash(_('Your subscription is disabled. Please update your payment method.'), 'important')

    engine, metadata = get_db()
    payments = metadata.tables['payment']
    stmt = select(payments).where(
        payments.c.user_id == g.user.id,
    )
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        error = f"Something went wrong."
        payments = []
    else:
        payments = result.fetchall()

    return render_template(
        'payment/index.html',
        payments=payments,
    )

@bp.route('/new_payment_method', methods=['POST'])
@login_required
@payment_enabled
def new_payment_method():
    error = None

    if not request.form['stripe_token']:
        error = _('Stripe token is required.')

    if error is not None:
        flash(error)
    else:
        stripe = get_stripe()

        try:
            if not g.user.stripe_customer:
                stripe_customer = stripe.Customer.create( 
                    description="~" + g.user.username, 
                    email=g.user_pref.email, 
                    card=request.form['stripe_token']
                )
            else:
                stripe_customer = stripe.Customer.retrieve(g.user.stripe_customer)
                source = stripe.Customer.create_source(
                    g.user.stripe_customer,
                    source=request.form['stripe_token']
                )
                result = stripe.Customer.modify(
                    g.user.stripe_customer,
                    default_source=source['id'],
                )

            engine, metadata = get_db()
            user = metadata.tables['user']

            stmt = user.update().values(
                stripe_customer=stripe_customer['id']
            ).where(
                user.c.id == g.user.id,
            )
            with engine.connect() as conn:
                result = conn.execute(stmt)
                conn.commit()

        except SQLAlchemyError as e:
            current_app.logger.error(str(e))
            error = _("Something went wrong.")
        except stripe.error.CardError as e:
            current_app.logger.error(str(e))
            error = _("Payment went wrong.")
        else:
            if user_charged(g.user) or user_grace_period(g.user):
                flash(_("Payment method created."))
                return redirect(url_for("payment.index"))
            else:
                try:
                    load_logged_in_user() # refresh stripe_customer
                    charge_user(g.user, g.user_pref)
                except SQLAlchemyError as e:
                    current_app.logger.error(str(e))
                    error = _("Something went wrong.")
                except stripe.error.CardError as e:
                    current_app.logger.error(str(e))
                    error = _("Payment went wrong.")
                except smtplib.SMTPException as e:
                    current_app.logger.error(str(e))
                    error = _("Email notice went wrong.")
                else:
                    flash(_("Payment method created, and card has been charged."))
                    return redirect(url_for("payment.index"))

    flash(error)

    return redirect(url_for("payment.index"))

@bp.route('/drop_payment_methods', methods=['POST'])
@login_required
@payment_enabled
def drop_payment_methods():
    if not g.user.stripe_customer:
        flash(_("You don't have any payment method registered yet."))
        return redirect(url_for("payment.index"))

    stripe = get_stripe()

    try:
        stripe.Customer.delete(g.user.stripe_customer)

        engine, metadata = get_db()
        user = metadata.tables['user']

        stmt = user.update().values(
            stripe_customer=None
        ).where(
            user.c.id == g.user.id,
        )
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        error = f"Something went wrong."
    except stripe.error.CustomerError as e:
        current_app.logger.error(str(e))
        error = f"Stripe went wrong."
    else:
        flash(_("Payment method deleted."))
        return redirect(url_for("payment.index"))

    flash(error)

    return redirect(url_for("payment.index"))

@bp.route('/<int:id>/invoice', methods=['GET'])
@login_required
@payment_enabled
def invoice(id):
    engine, metadata = get_db()
    payments = metadata.tables['payment']
    stmt = select(payments).where(
        payments.c.id == id,
        payments.c.user_id == g.user.id,
    )
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        abort(500, "Something went wrong.")
    else:
        payment = result.fetchone()

    return render_template(
        'payment/invoice.html',
        payment=payment,
    )

@bp.route('/<int:id>/invoice.pdf', methods=['GET'])
@login_required
def invoice_pdf(id):
    return render_pdf(
        url_for('payment.invoice', id=id),
        download_filename="fossbill_invoice_{}.pdf".format(id)
    )

@bp.cli.command('charge-users')
def charge_users():
    engine, metadata = get_db()

    users = metadata.tables['user']
    user_prefs = metadata.tables['user_pref']

    j = join(users, user_prefs, users.c.id == user_prefs.c.user_id)
    stmt = select(users, user_prefs).select_from(j).where(
        users.c.stripe_customer != None,
        ((users.c.due_at == None) | (datetime.date.today() > users.c.due_at)) &
        (datetime.date.today() - datetime.timedelta(days=grace_days()) > users.c.created_at)
    )

    try:
        with engine.connect() as conn:
            to_charge_users = conn.execute(stmt).fetchall()
    except SQLAlchemyError as e:
        print(str(e))
        print(f"Something went wrong.")
        return

    print("Starting charging...")
    for to_charge_user in to_charge_users:
            print("Charging user {} card.".format(to_charge_user.id))
            try:
                charge_user(to_charge_user, to_charge_user)
            except SQLAlchemyError as e:
                print("Something went wrong: " + str(e))
            except stripe.error.CardError as e:
                print("Payment went wrong: " + str(e))
            except smtplib.SMTPException as e:
                print("Email notice went wrong: " + str(e))

    print("Done!")
