from setuptools import setup, find_packages

setup(
  name = 'math_for_cannibals',
  version = '1.14', 
  packages = find_packages(),
  description = 'Math functions to simplify mathematical tasks', 
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  author = 'Hannibal Lykke Kofoed',
  author_email = 'hanniballykkekofoed@icloud.com', 
  # It is possible to add entrypoints.
  install_requires=[
        'numpy',
  ],
  license='MIT',
  url = 'https://gitlab.com/hann1ba1/math-for-cannibals',
  keywords = ['python', 'math', 'mathematics'],
   classifiers=[
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
  ]
)

# pip install setuptools wheel twine
# python setup.py sdist bdist_wheel

# twine upload dist/*

