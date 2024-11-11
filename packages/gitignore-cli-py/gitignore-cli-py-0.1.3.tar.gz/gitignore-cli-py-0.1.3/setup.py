from setuptools import setup
from setuptools.command.install import install
import os

class PostInstallCommand(install):
    """Custom post-installation command."""
    def run(self):
        install.run(self)
        self.execute_post_install()

    def execute_post_install(self):
        print("\n===========================")
        print("Thank you for installing gitignore-cli-py!")
        print("To use the tool, run the following command:")
        print("\n    gitignore-cli --help\n")
        print("Make sure that '/home/$USER/.local/bin' is in your PATH.")
        print("If not, follow the steps below to add it to your PATH.")
        print("\nFor Bash users:")
        print("1. Open your ~/.bashrc file:")
        print("\n    nano ~/.bashrc")
        print("2. Add the following line at the end of the file:")
        print("\n    export PATH=\"$HOME/.local/bin:$PATH\"")
        print("3. Save the file and run:")
        print("\n    source ~/.bashrc\n")

        print("For Zsh users:")
        print("1. Open your ~/.zshrc file:")
        print("\n    nano ~/.zshrc")
        print("2. Add the following line at the end of the file:")
        print("\n    export PATH=\"$HOME/.local/bin:$PATH\"")
        print("3. Save the file and run:")
        print("\n    source ~/.zshrc\n")

        print("\nTo enable autocomplete for gitignore-cli, follow the steps below:")
        print("\nFor Bash users:")
        print("1. Run the following command to enable autocomplete:")
        print("\n    _GITIGNORE_CLI_COMPLETE=bash_source gitignore-cli > ~/.gitignore-cli-complete.sh")
        print("2. Add the following line to your ~/.bashrc file:")
        print("\n    source ~/.gitignore-cli-complete.sh")
        print("3. Reload your Bash configuration:")
        print("\n    source ~/.bashrc\n")

        print("For Zsh users:")
        print("1. Run the following command to enable autocomplete:")
        print("\n    _GITIGNORE_CLI_COMPLETE=zsh_source gitignore-cli > ~/.gitignore-cli-complete.sh")
        print("2. Add the following line to your ~/.zshrc file:")
        print("\n    source ~/.gitignore-cli-complete.sh")
        print("3. Reload your Zsh configuration:")
        print("\n    source ~/.zshrc\n")

        print("For more information, visit the project repository:")
        print("https://github.com/ninjapythonbrasil/gitignore-cli")
        print("===========================\n")

setup(
    name="gitignore-cli-py",
    version="0.1.3",
    author="Raphael Augusto Ferroni Cardoso",
    author_email="rferronicardoso@gmail.com",
    description="A command-line tool to generate .gitignore files from predefined templates",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ninjapythonbrasil/gitignore-cli-py",
    license="MIT",
    license_file="LICENSE",
    packages=["gitignore_cli"],
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "gitignore-cli=gitignore_cli.cli:cli",
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Version Control",
    ],
    python_requires='>=3.8',
)
