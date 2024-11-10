from setuptools import setup, find_packages

setup(
    name="PrasBridge",
    version="1.0.5",
    packages=find_packages(),
    install_requires=[
        "Django>=3.2",
        "SQLAlchemy>=2.0.35", 
    ],
    keywords=['Pras', 'Django', 'ORM', 'SQLAlchemy', 'PrasSerializer', 'PrasForms', 'PrasToken', 'PrasHash', 'PrasBase', 'PrasSerializer', 'PrasForms', 'PrasToken', 'PrasHash', 'PrasBase', 'PrasBridge'],
    author="PRAS Samin",
    author_email="prassamin@gmail.com",
    description="PrasBridge: Simplify project development with a powerful toolkit for integrating SQLAlchemy with Django-style features. Offers serializers, enhanced forms, token generation, hashing, ready-to-use base models and more features. perfect for projects using SQLAlchemy as the main ORM.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PRASSamin/PrasBridge",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
