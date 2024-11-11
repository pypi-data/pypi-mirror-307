import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='multi-interface-inversion',
    version="0.0.3",
    author='Wang Chao',
    description='calculate gravity anomalies from multi-interfaces and estimate double-interfaces model'
                ' from gravity anomalies, given prior information about constraints between the '
                'density interfacesthe using Crust1.0 model, where Vertical Gravity Gradient data are used as'
                'inputs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/WangChao/MII',
    include_package_data=True,
    package_data={
        'multi_interface_inversion': ['dataset/crust1.bnds',
                                         'dataset/crust1.rho',
                                        'dataset/curv_32.nc']
    },
    python_requires='>=3.8',
    install_requires=[
        'cftime==1.6.4.post1',
        'contourpy==1.1.1',
        'cycler==0.12.1',
        'fonttools==4.54.1',
        'imageio==2.35.1',
        'importlib-resources==6.4.5',
        'kiwisolver==1.4.7',
        'lazy-loader==0.4',
        'matplotlib==3.7.5',
        'netCDF4==1.5.7',
        'networkx==3.1',
        'numpy==1.24.4',
        'packaging==24.2',
        'pandas==2.0.3',
        'pillow==10.4.0',
        'pygmt==0.9.0',
        'pyparsing==3.1.4',
        'python-dateutil==2.9.0.post0',
        'pytz==2024.2',
        'PyWavelets==1.4.1',
        'scikit-image==0.21.0',
        'scipy==1.10.1',
        'six==1.16.0',
        'tifffile==2023.7.10',
        'tzdata==2024.2',
        'xarray==2023.1.0',
        'zipp==3.20.2'
    ]
)


