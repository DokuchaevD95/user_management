"""Инициализация jinja энвайронмента. Singleton"""

__all__ = ['jinja_env']

from jinja2 import Environment, FileSystemLoader


jinja_env = Environment(
    loader=FileSystemLoader('templates'),
    enable_async=True
)
