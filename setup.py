from glob import glob
from setuptools import find_packages, setup

package_name = "roslab_api"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/launch", glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Workshop Team",
    maintainer_email="workshop@example.com",
    description="Minimal rosbridge and API package for an existing ROS 2 environment.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "bridge_api_server = roslab_api.api_server:main",
        ],
    },
)
