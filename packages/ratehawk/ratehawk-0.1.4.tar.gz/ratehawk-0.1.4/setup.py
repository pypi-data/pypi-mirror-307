from setuptools import setup, find_packages

setup(
    name="ratehawk",
    version="0.1.4",
    packages=find_packages(include=['ratehawk', 'ratehawk.*']),
    install_requires=[
        "redis>=4.0.0",
        "aiosqlite>=0.17.0",
        "asyncpg>=0.27.0",
        "prometheus-client>=0.12.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-asyncio>=0.14.0",
            "black>=20.8b1",
            "isort>=5.6.4",
        ],
        "monitoring": [
            "prometheus-client>=0.12.0",
            "grafana-api-client>=0.3.4",
            "python-dateutil>=2.8.2",
        ],
    },
    author="Andrew Wade",
    author_email="hi@wadedev.online",
    description="A flexible API rate limiting library for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/wadedesign/ratehawk",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)
