import platform
import subprocess

def check_r_installed():
    current_platform = platform.system()

    if current_platform == "Windows":
        # Check if R is installed on Windows by checking the registry
        try:
            subprocess.run(
                ["reg", "query", "HKLM\\Software\\R-core\\R"], check=True
            )
            print("R is already installed on Windows.")
            return True
        except subprocess.CalledProcessError:
            print("R is not installed on Windows.")
            return False

    elif current_platform == "Linux":
        # Check if R is installed on Linux by checking if the 'R' executable is available
        try:
            subprocess.run(["which", "R"], check=True)
            print("R is already installed on Linux.")
            return True
        except subprocess.CalledProcessError:
            print("R is not installed on Linux.")
            return False

    elif current_platform == "Darwin":  # macOS
        # Check if R is installed on macOS by checking if the 'R' executable is available
        try:
            subprocess.run(["which", "R"], check=True)
            print("R is already installed on macOS.")
            return True
        except subprocess.CalledProcessError:
            print("R is not installed on macOS.")
            return False

    else:
        print("Unsupported platform. Unable to check for R installation.")
        return False

def install_r():

    current_platform = platform.system()

    if current_platform == "Windows":
        # Install R on Windows using PowerShell
        install_command = "Start-Process powershell -Verb subprocess.runAs -ArgumentList '-Command \"& {Invoke-WebRequest https://cran.r-project.org/bin/windows/base/R-4.1.2-win.exe -OutFile R.exe}; Start-Process R.exe -ArgumentList '/SILENT' -Wait}'"
        subprocess.run(install_command, shell=True)

    elif current_platform == "Linux":
        # Install R on Linux using the appropriate package manager (e.g., apt-get)
        install_command = (
            "sudo apt update -qq && sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9"
            + "&& sudo add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/'"
            + "&& sudo apt update"
            + "&& sudo apt -y install r-base"
        )
        subprocess.run(install_command, shell=True)

    elif current_platform == "Darwin":  # macOS
        # Install R on macOS using Homebrew
        install_command = "brew install r"
        subprocess.run(install_command, shell=True)

    else:

        print("Unsupported platform. Unable to install R.")

def install_packages():
    try: 
        subprocess.run(["Rscript", "-e", "utils::install.packages('remotes', dependencies=TRUE)"])
        subprocess.run(["Rscript", "-e", "utils::install.packages(c('R6', 'Rcpp', 'skimr'), dependencies=TRUE)"])
        subprocess.run(["Rscript", "-e", "remotes::install_github('Techtonique/learningmachine')"])        
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.output}")
        print(f"Stderr: {e.stderr}")
        try:
            subprocess.run(["mkdir", "-p", "r-learningmachine"])		 
            subprocess.run(["Rscript", "-e", "utils::install.packages('remotes', lib='r-learningmachine', dependencies=TRUE)"])
            subprocess.run(["Rscript", "-e", "utils::install.packages(c('R6', 'Rcpp', 'skimr'), lib='r-learningmachine', dependencies=TRUE)"])
            subprocess.run(["Rscript", "-e", "remotes::install_github('Techtonique/learningmachine', lib='r-learningmachine')"])
        except subprocess.CalledProcessError as e:    
            print(f"Error occurred: {e}")
            print(f"Return code: {e.returncode}")
            print(f"Output: {e.output}")
            print(f"Stderr: {e.stderr}")        
            try:	
                subprocess.run(["Rscript", "-e", "utils::install.packages('remotes', dependencies=TRUE)"])
                subprocess.run(["Rscript", "-e", "utils::install.packages(c('R6', 'Rcpp', 'skimr'), dependencies=TRUE)"])
                subprocess.run(["Rscript", "-e", "remotes::install_github('Techtonique/learningmachine')"])        
            except subprocess.CalledProcessError as e:	
                print(f"Error occurred: {e}")
                print(f"Return code: {e.returncode}")
                print(f"Output: {e.output}")
                print(f"Stderr: {e.stderr}")        
                try: 
                    subprocess.run(["mkdir", "-p", "r-learningmachine"])		 
                    subprocess.run(["Rscript", "-e", "utils::install.packages('remotes', lib='r-learningmachine', dependencies=TRUE)"])
                    subprocess.run(["Rscript", "-e", "utils::install.packages(c('R6', 'Rcpp', 'skimr'), lib='r-learningmachine', dependencies=TRUE)"])
                    subprocess.run(["Rscript", "-e", "remotes::install_github('Techtonique/learningmachine', lib='r-learningmachine')"])
                except subprocess.CalledProcessError as e:
                    print(f"Error occurred: {e}")
                    print(f"Return code: {e.returncode}")
                    print(f"Output: {e.output}")
                    print(f"Stderr: {e.stderr}")        
                    try:	
                        subprocess.run(["Rscript", "-e", "utils::install.packages('remotes', dependencies=TRUE)"])
                        subprocess.run(["Rscript", "-e", "utils::install.packages(c('R6', 'Rcpp', 'skimr'), dependencies=TRUE)"])
                        subprocess.run(["Rscript", "-e", "remotes::install_github('Techtonique/learningmachine')"])
                    except subprocess.CalledProcessError as e:	
                        print(f"Error occurred: {e}")
                        print(f"Return code: {e.returncode}")
                        print(f"Output: {e.output}")
                        print(f"Stderr: {e.stderr}")        
                        subprocess.run(["mkdir", "-p", "r-learningmachine"])		 
                        subprocess.run(["Rscript", "-e", "utils::install.packages('remotes', lib='r-learningmachine', dependencies=TRUE)"])
                        subprocess.run(["Rscript", "-e", "utils::install.packages(c('R6', 'Rcpp', 'skimr'), lib='r-learningmachine', dependencies=TRUE)"])
                        subprocess.run(["Rscript", "-e", "remotes::install_github('Techtonique/learningmachine', lib='r-learningmachine')"])


# Check if R is installed; if not, install it
if not check_r_installed():
    install_r_prompt = int(input("Try installing R? 1-yes, 2-no"))
    if install_r_prompt == 1: 
        print("Installing R...")
        install_r()
    else:
        raise ValueError('Try installing R manually first.')
else:
    print("No R installation needed.")

install_packages()

subprocess.run(["pip", "install", "rpy2"])

from setuptools import setup, find_packages
from codecs import open
from os import path

# 4 - Package setup -----------------------------------------------
    
"""The setup script."""

setup(
    author="T. Moudiki",
    author_email="thierry.moudiki@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Machine Learning with uncertainty quantification and interpretability",
    install_requires=['numpy', 'pandas', 'rpy2>=3.4.5', 'scikit-learn', 'scipy'],
    license="BSD Clause Clear license",
    long_description="Machine Learning with uncertainty quantification and interpretability.",
    include_package_data=True,
    keywords="learningmachine",
    name="learningmachine",
    packages=find_packages(include=["learningmachine", "learningmachine.*"]),
    test_suite="tests",
    url="https://github.com/Techtonique/learningmachine_python",
    version="2.7.0",
    zip_safe=False,
)
