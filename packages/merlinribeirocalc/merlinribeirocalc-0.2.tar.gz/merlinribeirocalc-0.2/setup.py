from setuptools import setup, find_packages

setup(
    name="merlinribeirocalc",               # Nome único da biblioteca no PyPI
    version="0.2",
    packages=find_packages(),
    description="Uma biblioteca de calculadora padrão",
    author="Merlin Ribeiro",
    author_email="ribeiro.filho@academico.ifpb.edu.br",
    url="https://github.com/merlin-ribeiro/",  # Opcional
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",           # Se aplica à licença que escolher
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',                                # Defina a versão mínima do Python
)
