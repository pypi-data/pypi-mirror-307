from setuptools import setup, find_packages

setup(
    name="smartdebugger",  # Nome do pacote no PyPI
    version="0.1.0",       # Versão inicial
    author="Saide Omar Saide",
    author_email="saideomarsaid@gmail.com",
    description="Uma biblioteca para depuração usando modelos de linguagem",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seuusuario/smartdebugger",  # URL do projeto
    packages=find_packages(),  # Inclui todas as subpastas com __init__.py
    install_requires=[
        "google-generativeai",
        "Pillow",
        "langchain-core",
        "langchain-groq",
        "openai",
        "colorama",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Versão mínima do Python
)
