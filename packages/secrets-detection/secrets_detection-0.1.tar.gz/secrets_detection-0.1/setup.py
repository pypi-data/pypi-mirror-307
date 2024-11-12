from setuptools import setup, find_packages

setup(
    name='secrets-detection',  
    version='0.1',  
    packages=find_packages(),  
    install_requires=['requests'],  
    entry_points={
        'console_scripts': [
            'scan-secrets = secrets_scanner.scanner:analyze_repository',
        ],
    },
    author='boyinf',   
    description='A package for use in detecting secrets leaks in the GitLab pipeline.',  
    long_description="The secrets detection tool was developed with the aim of assisting in the analysis of secrets leaking through the pipeline. Created to assist in leak detection, the tool stands out for its simplicity and efficiency through regex and analysis of the entire repository, representing the result intuitively through JSON reports.",  
    long_description_content_type='text/plain',
    url='https://github.com/Boyinf/secrets-detection/',  
    license='MIT',  
    classifiers=[  
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',  
    ],
)