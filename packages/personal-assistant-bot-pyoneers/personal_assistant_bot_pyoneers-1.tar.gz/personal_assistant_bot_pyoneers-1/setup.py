from setuptools import setup, find_namespace_packages


setup(
    name="personal_assistant_bot_pyoneers",
    version="1",
    description="A DEMO version of Personal Assistant Bot.",
    long_description="command-line tool designed to assist you in organizing your contacts and notes efficiently. It allows you to easily manage and access contacts information (name, phone numbers, birthday, email address, and physical address) and additionally, to manage your personal notes as well as categorize them by titles or tags for better organization. Application works offline and doesn't require stable internet connection. All data is stored locally on your PC thus information remains secure and accessible whenever you need it.",
    url="https://github.com/SergeyPoly/goit-pycore-final-project.git",
    author="PyOneers-team",
    author_email="spoly82@gmail.com",
    license="MIT",
    packages=find_namespace_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=["prompt_toolkit", "prettytable", "colorama", "wcwidth"],
    entry_points={"console_scripts": ["bot_run = project:main"]},
)
