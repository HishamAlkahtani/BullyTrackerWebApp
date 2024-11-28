from setuptools import setup

setup(
    name="bullytracker",
    packages=["bullytracker"],
    include_package_data=True,
    install_requires=[
        "flask",
        "flask_login",
        "uuid",
        "firebase-admin",
        "twilio",
        "shapely",
        "flask-cors",
    ],
)
