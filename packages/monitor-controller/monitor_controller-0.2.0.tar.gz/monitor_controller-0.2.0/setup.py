from setuptools import setup, find_packages

setup(
    name="monitor_controller",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "inquirer",
        "monitorcontrol",
        "wmi",
    ],
    entry_points={
        "console_scripts": [
            "monitor_controller=monitor_controller.__main__:main",
        ],
    },
    author="Ate Pelsma",
    author_email="ate.pelsma@gmail.com",
    description="A Python application to control monitor input sources based on connected devices.",
    license="MIT",
    url="https://github.com/ate-pelsma/monitor_controller",
)