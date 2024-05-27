from setuptools import setup, find_packages

setup(
    name='alex_assistant',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'anthropic',
        'mss',
        'SpeechRecognition',
        'Pillow',
        'rich',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'alex=alex:main',
        ],
    },
    author='Ben Blaiszik',
    author_email='your.email@example.com',
    description='A simple tutorial showing how to capture the screen, recognize speech, add context, and query Anthropic API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/blaiszik/alex-assistant',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)