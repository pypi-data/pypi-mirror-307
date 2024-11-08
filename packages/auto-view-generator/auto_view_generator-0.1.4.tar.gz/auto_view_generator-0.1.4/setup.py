from setuptools import setup, find_packages

setup(
    name='auto-view-generator',
    version='0.1.4',
    packages=find_packages(include=["django_view_generator", "django_view_generator.*"]),
    include_package_data=True,
    install_requires=[
        'django>=3.0',  # Django version requirement
    ],
    entry_points={
        'django.manage': [
            'generate_views_and_serializers=django_view_generator.management.commands.generate_views_and_serializers:Command',
        ],
    },
    author='Adarsh Shukla',
    author_email='adarshukla999@gmail.com',
    description='A Django management command to generate views and serializers based on models.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AdarshShukla777/auto_view_generator',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
)
