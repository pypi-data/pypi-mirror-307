from setuptools import setup, find_packages

setup(
    name='yet_another_shcheck_generator',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'financial_calculator = financial_calculator.calculator:main'
        ]
    },
    install_requires=[],  # Зависимостей нет
)