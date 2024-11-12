from setuptools import setup, find_packages

setup(
    name="plagiarism_check_app",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "nltk",
        "pytest",
    ],
    entry_points={
        "console_scripts": [
            "start-my-fastapi=app.main:main",
        ],
    },
    description="A FastAPI app",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vira Boiko",
    author_email="vira.shendrykk@gmail.com",
    url="https://github.com/viraboik/plagiarismcheck.git",
)
