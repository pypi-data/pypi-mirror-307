from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

VERSION = '0.0.4'
DESCRIPTION = "ArcheAI is a lightweight Python framework that simplifies AI agent development. Build smarter, more capable agents with ease using ArcheAI's easy tool integration, LLM interaction, and agent orchestration."

# Setting up
setup(
    name="archeai",
    version=VERSION,
    author="E5Anant (Anant Sharma)",
    author_email="e5anant2011@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['cohere', 'groq', 'rich==12.6.0', 'python-dotenv==1.0.1', 'google-generativeai', 'requests==2.31.0', 'colorama==0.4.6', 'googlesearch-python==1.2.4', 'yfinance==0.2.41', 'bs4==0.0.1', 'anthropic', 'openai', 'scikit-learn==1.5.2'],
    keywords=['agents', 'archeai', 'archeAI', 'multi-agent', 'taskforce', 'python', 'light-weight', 'agent-framework', 'ArcheAI'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

)