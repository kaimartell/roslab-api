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
    maintainer="Kai Martell",
    maintainer_email="kai.martell@tufts.edu",
    description="Generic rosbridge and rosapi connector for the ROS Lab frontend.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={},
)
