import sqlite3
from datetime import datetime
import os

import click
from flask import current_app, g
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool

def get_db():
    if 'db' not in g:
        db_url = current_app.config['SQLALCHEMY_DATABASE_URI']
        
        # Use appropriate connection settings based on database type
        if db_url.startswith('sqlite'):
            # SQLite connection
            engine = create_engine(
                db_url,
                connect_args={'check_same_thread': False},
                poolclass=StaticPool
            )
        else:
            # PostgreSQL connection
            engine = create_engine(db_url, pool_pre_ping=True)
        
        g.db = engine.connect()

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """Initialize database with schema"""
    db = get_db()
    
    # Read schema
    with current_app.open_resource('schema.sql') as f:
        schema = f.read().decode('utf8')
    
    db_url = current_app.config['SQLALCHEMY_DATABASE_URI']
    
    if db_url.startswith('sqlite'):
        # SQLite - execute directly
        conn = sqlite3.connect(db_url.replace('sqlite:///', ''))
        conn.executescript(schema)
        conn.commit()
        conn.close()
    else:
        # PostgreSQL - convert schema to PostgreSQL syntax
        schema_pg = schema.replace('AUTOINCREMENT', '')
        statements = schema_pg.split(';')
        for statement in statements:
            if statement.strip():
                db.execute(text(statement))
        db.commit()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

