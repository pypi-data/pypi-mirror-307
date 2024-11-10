from setuptools import setup


def requirements():
    with open("requirements.txt") as f:
        return [x for x in f.read().strip().split("\n") if x]


setup(
    name="research-report",
    version="1.0.0",
    author="TimurTimergalin",
    author_email="tmtimergalin8080@gmail.com",
    description="A small library for convenient construction of experiments report",
    url="https://github.com/TimurTimergalin/research_report",
    packages=["research_report"],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords="python report ipython",
    install_requires=requirements()
)
