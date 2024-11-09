from setuptools import setup, find_packages

setup(
    name="swastha",  # Ensure your package name is unique
    version="0.1.0",  # Update the version number
    author="the_py_developer",
    author_email="pyprogramtestrun@gmail.com",
    description="A chatbot interface using Google Generative AI with a Tkinter interface for API key input",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/py-developer-basil/google_chatbot.git",  # Your GitHub repo URL
    packages=find_packages(),
    install_requires=[
        "google-generativeai",  # Keep the essential dependencies
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
