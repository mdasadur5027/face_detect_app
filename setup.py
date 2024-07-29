from setuptools import setup, find_packages

setup(
    name='face_detection_app',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'opencv-python',
        'dlib',
        'Pillow',
        'tk',
    ],
    entry_points={
        'console_scripts': [
            'face_detection_app=app.main:main',
        ],
    },
)
