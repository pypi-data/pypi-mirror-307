from setuptools import setup

setup(
    name='generate_receipt_annyandr',
    version='1.0',
    py_modules=['generate_receipt'],
    entry_points={
        'console_scripts': [
            'generate_receipt = receipt:main'
        ]
    }
)