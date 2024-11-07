from setuptools import setup

setup(
    name='opnsense_helper',
    version='0.1.1',    
    description='assign lan interfaces, create vlans, vlan-interfaces and setup dhcp in a single script.',
    url='https://github.com/the-pod-shop/opnsense-helper/',
    author='ji-podhdead',
    author_email='ji.podhdead@proton.me',
    license='BSD 2-clause',
    packages=['opnsense_helper'],
    install_requires=['paramiko',                     
                      ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
