from setuptools import find_packages, setup  ## find_packages: It will automatically find all the packages in the machine learning application
from typing import List

HYPEN_E_DOT='-e.' 

def get_requirements(file_path: str) -> List[str]:
    '''
    This function will return a list of requirements
    '''
    requirements = []
    with open(file_path) as file_object:
        requirements = file_object.readlines()  ## it also store \n
        requirements = [req.replace("\n", "")for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements


setup(
name = 'mlproject',
version='0.0.1',
author= 'Suraj',
author_email='singhsuraj182005@gmail.com',
packages= find_packages(),
install_requires= get_requirements('requirements.txt')  ## what all libraries we want, it will automatically download 

)