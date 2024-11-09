from setuptools import setup, find_packages

setup(
    name='fezajs',
    version='0.0.1',
    packages=["fezajs"],
    url='',
    license='MIT',
    author='Mert',
    author_email="contact@tomris.dev",
    description='FezaJS is a simple JSON ORM for Python',
    long_description=open("fezajs/README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    python_requires=">=3.9",
    keywords=["json", "orm", "fezajs"],
    zip_safe=True,
    platforms="any"
)
