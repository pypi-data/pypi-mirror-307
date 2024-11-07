from setuptools import setup, find_packages


setup(
    name='perennityai-viz',
    version='0.1.0',  # Developmental release (devN)
    author='Perennity AI',
    author_email='info@perennityai.com',
    description='A data visualization tool for MediaPipe hand, face, and pose landmarks with Perennity AI enhancements.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/perennityai/perennityai-viz',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    python_requires='>=3.8',
    install_requires=[
        'tensorflow>=2.5.0,<=2.17.0', 
        "tensorboard>=2.5.0,<=2.17.0",
        "keras",
        'matplotlib',
        "matplotlib",
        "opencv-python",
        "json5 ",
        "pandas",
        "mediapipe"
    ],
    entry_points={
        'console_scripts': [
            'perennityai-viz = perennity_viz.main:main',
        ],
    },
    include_package_data=True,
    package_data={
        # Include any config or other necessary data files in the package
        '': ['configs/*.ini'],
    },
    license='MIT',
    keywords='mediapipe visualization hand landmarks face landmarks pose landmarks data-viz PerennityAI',
)