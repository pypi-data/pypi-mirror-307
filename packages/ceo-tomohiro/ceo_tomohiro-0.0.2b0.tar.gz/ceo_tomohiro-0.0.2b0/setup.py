import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("LICENSE", "r", encoding="utf-8") as fh:
    license_content = fh.read()

setuptools.setup(
    name="ceo-tomohiro",
    version='0.0.2-beta',
    author="vortezwohl",
    author_email="vortez.wohl@gmail.com",
    description="Tomohiro is an assistant in your shell.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=license_content,
    url="https://github.com/vortezwohl/CEO-Tomohiro",
    project_urls={
        "Bug Tracker": "https://github.com/vortezwohl/CEO-Tomohiro/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.10",
    install_requires=[
        'ceo-py>=0.6.0rc0',
        'python-dotenv>=1.0.1',
        'sympy==1.13.3',
        'colorama>=0.4.6',
        'duckduckgo_search>=6.3.3'
    ],
    entry_points={
        'console_scripts': [
            'tomohiro = tomohiro_shell.tomohiro_shell:main'
        ]
    },
    include_package_data=False
)