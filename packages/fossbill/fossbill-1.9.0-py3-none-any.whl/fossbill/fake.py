from flask import (
    Blueprint, current_app
)
from fossbill.database import get_db
from sqlalchemy import join, insert, select, func
from sqlalchemy.exc import SQLAlchemyError
import click
from faker import Faker
import random
import datetime

bp = Blueprint('fake', __name__)

@bp.cli.command('product')
@click.argument('user_id')
@click.option('--count', default=1, help='Number of element.')
def product(user_id, count):
    engine, metadata = get_db()

    users = metadata.tables['user']
    stmt = select(users).where(users.c.id == user_id)
    with engine.connect() as conn:
        result = conn.execute(stmt)
    user = result.fetchone()

    user_prefs = metadata.tables['user_pref']
    stmt = select(user_prefs).where(user_prefs.c.user_id == user_id)
    with engine.connect() as conn:
        result = conn.execute(stmt)
    user_pref = result.fetchone()

    fake = Faker(user_pref.locale)

    for i in range(count):
        stmt = insert(metadata.tables['product']).values(
            label=" ".join(fake.words()),
            price=random.randint(0, 50000),
            tax_rate=random.randint(0, 50),
            user_id=user_id,
        )
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()

@bp.cli.command('customer')
@click.argument('user_id')
@click.option('--count', default=1, help='Number of element.')
def customer(user_id, count):
    engine, metadata = get_db()

    users = metadata.tables['user']
    stmt = select(users).where(users.c.id == user_id)
    with engine.connect() as conn:
        result = conn.execute(stmt)
    user = result.fetchone()

    user_prefs = metadata.tables['user_pref']
    stmt = select(user_prefs).where(user_prefs.c.user_id == user_id)
    with engine.connect() as conn:
        result = conn.execute(stmt)
    user_pref = result.fetchone()

    fake = Faker(user_pref.locale)

    for i in range(count):
        stmt = insert(metadata.tables['customer']).values(
            address=fake.address(),
            email=fake.email(),
            label=fake.name(),
            user_id=user_id,
        )
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()

@bp.cli.command('bill')
@click.argument('user_id')
@click.option('--count', default=1, help='Number of element.')
def bill(user_id, count):
    engine, metadata = get_db()

    users = metadata.tables['user']
    stmt = select(users).where(users.c.id == user_id)
    with engine.connect() as conn:
        result = conn.execute(stmt)
    user = result.fetchone()

    user_prefs = metadata.tables['user_pref']
    stmt = select(user_prefs).where(user_prefs.c.user_id == user_id)
    with engine.connect() as conn:
        result = conn.execute(stmt)
    user_pref = result.fetchone()

    fake = Faker(user_pref.locale)

    for i in range(count):
        stmt = select(join(metadata.tables['customer'], users)).where(users.c.id == user_id).order_by(func.random())
        with engine.connect() as conn:
            result = conn.execute(stmt)
            customer = result.fetchone()

        stmt = insert(metadata.tables['bill']).values(
            customer_id=customer.id if customer else None,
            created_at=fake.date_between(
                datetime.date.today() - datetime.timedelta(days=random.randint(0, 90)),
                datetime.date.today()
            ),
            recipient=customer.address if customer else fake.address(),
            source=user_pref.source,
            bill_mentions=user_pref.bill_mentions,
            quote_mentions=user_pref.quote_mentions,
            user_id=user_id,
        )
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            bill_id = result.inserted_primary_key[0]

        for y in range(random.randint(1, 10)):
            stmt = select(join(metadata.tables['product'], users)).where(users.c.id == user_id).order_by(func.random())
            with engine.connect() as conn:
                result = conn.execute(stmt)
                product = result.fetchone()

            stmt = insert(metadata.tables['bill_row']).values(
                user_id=user_id,
                bill_id=bill_id,
                label=product.label if product else " ".join(fake.words()),
                price=product.price if product else random.randint(0, 50000),
                quantity=random.randint(0, 40),
                tax_rate=product.tax_rate if product else random.randint(0, 50),
            )
            with engine.connect() as conn:
                result = conn.execute(stmt)
                conn.commit()
