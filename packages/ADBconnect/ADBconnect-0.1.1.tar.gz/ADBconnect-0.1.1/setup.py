from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='ADBconnect',
  version='0.1.1',
  author='Ijidishurka',
  description='Controlling your phone via ADB.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Ijidishurka/ADBconnect',
  packages=find_packages(),
  install_requires=['opencv-python', 'numpy'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='adb phone ADB',
  project_urls={
    'GitHub': 'https://github.com/Ijidishurka/ADBconnect'
  },
  python_requires='>=3.6'
)