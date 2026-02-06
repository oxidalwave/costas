import sys, os
from setuptools import setup

dependencies = [
    'Pillow',
    'swig',
    'lgpio',
    'rpi-lgpio',
    'spidev',
    'MLB-StatsAPI',
    'gpiozero',
    'waveshare-epaper'
]

setup(
    name='waveshare-epd',
    description='Waveshare e-Paper Display',
    author='Waveshare',
    install_requires=dependencies,
)

