from setuptools import setup, find_packages

setup(
    name="TheDebugger",
    version="0.5.0",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
        "Pillow",
        "langchain-core",
        "langchain-groq",
        "openai",
        "colorama",
        "requests",
        "beautifulsoup4"
    ],
    author="Saide Omar Saide",
    author_email="saideomarsaideleon@gmail.com",
    description="Uma biblioteca para buscar e extrair dados do site 'Toda Matéria'.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/SaideOmaer1240/LearnFetch.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12.0',
)
