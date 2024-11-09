from setuptools import setup

setup(
    name='brynq_sdk_monday',
    version='1.1.0',
    description='Monday.com wrapper from BrynQ',
    long_description='Monday.com wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.monday"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
    ],
    zip_safe=False,
)
