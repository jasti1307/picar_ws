from setuptools import find_packages, setup

package_name = 'my_picar_driver'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='ubuntu@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'car_driver = my_picar_driver.car_driver:main',
            'camera_driver = my_picar_driver.camera_driver:main',
            'ultrasonic_node = my_picar_driver.ultrasonic_node:main',
            'safety_node = my_picar_driver.safety_node:main',
            'battery_node = my_picar_driver.battery_node:main',
            'gray_scale_node = my_picar_driver.gray_scale_node:main'

        ],
    },
)
