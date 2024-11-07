# setup.py

from setuptools import setup, find_packages

setup(
    name='first-django-generator', 
    version='0.1.1',
    package_dir={"":"management"},
    packages=find_packages(where="management"),
    include_package_data=True,
    install_requires=[
        'django>=3.0',  # Specify Django version requirement
    ],
    entry_points={
        'django.manage': [
            'generate_views_and_serializers = my_django_generator.management.commands.generate_views_and_serializers:Command',
        ],
    },
    author='Saurabh Shinde',
    author_email='saurabh004shinde@gmail.com',
    description='A Django management command to generate views and serializers based on models.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_django_generator',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
)
