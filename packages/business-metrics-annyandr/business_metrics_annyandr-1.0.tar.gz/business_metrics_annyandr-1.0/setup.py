from setuptools import setup

setup(
    name='business_metrics_annyandr',
    version='1.0',
    py_modules=['business_metrics'],
    entry_points={
        'console_scripts': [
            'business_metrics = business_metrics:main'
        ]
    }
)