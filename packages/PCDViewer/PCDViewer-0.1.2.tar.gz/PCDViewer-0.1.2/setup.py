from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='PCDViewer',
    version='0.1.2',
    description='A lightweight, Qt-based OpenGL viewer for visualising point cloud data.',
    author='Sepehr Sobhani',
    author_email='sepehr.sobhani@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sepehr-Sobhani-AU/PCDViewer",
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15.0',
        'numpy>=1.18.0',
        'PyOpenGL>=3.1.0',
        'Open3D',
    ],
    entry_points={
        'console_scripts': [
            'pcdviewer=PCDViewer:main',  # Assuming you create a `main()` function to start the app.
        ],
    },
    include_package_data=True,
    zip_safe=False
)
