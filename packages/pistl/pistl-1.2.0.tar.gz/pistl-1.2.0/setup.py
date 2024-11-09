# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pistl']

package_data = \
{'': ['*']}

install_requires = \
['ipykernel==6.27.1',
 'numpy==1.26.2',
 'pip==24.0.0',
 'pyvista[jupyter]>=0.38.1',
 'trame-components==2.2.1',
 'trame-vuetify==2.3.1',
 'trame==3.3.0',
 'vtk==9.3.0']

setup_kwargs = {
    'name': 'pistl',
    'version': '1.2.0',
    'description': 'Python library to generate STL format files for common shapes and geometries.',
    'long_description': '# <h1 style="text-align:center; color:\'red\'">PISTL (pronounced as "Pistol")</h1>\n\n<p text-align="center"><img src=".\\assets\\pystl_readme_cover.PNG" alt="Pystl_cover_image"></p>\n\n<u>About the figure above</u>: Multiple shapes generated using PISTL as STL file and visualized in **Meshmixer** for the purpose of this picture. The visualization in PISTL can be done using pyvista, which is installed as a dependency.\\_\n\n### What is PISTL?\n\nPISTL is a small (micro) library that can be used in python to programatically create stereolithographic (stl) files of regular geometric shapes like circle, cylinder, tetrahedron, sphere, pyramid and others by morphing these shapes. pystl also provide functions that can be used to translate and rotate these stl objects.\n\nIn summary:\nPISTL can be used for the following purposes:\n\n- to create simple geometric shape files in .stl format.\n- visualize this stl files. [PySTL uses pyvista for such visualizations].\n- perform simple transformations like translate, rotate and scale shapes.\n\n### Examples\n\n```python\n# This example creates a sphere stl using pistl\n\n# step 1.0: import PySTL\nimport pistl\nfrom pistl import shapes\n\n#instantiate a sphere shape\nsphere = shapes.Sphere()\n\n# set the radius of the sphere\nsphere.radius = 10\n\n# set resolution of the sphere in longitude and latitude\nsphere.resolution_latitude = 200\nsphere.resoultion_longitude = 200\n\n# once you have set the radius and resolution, call create method\nsphere.create()\n\n# call export method to set stl filename and shape name\nsphere.export(\'Results/sphere.stl\', \'sphere\')\n\n# Finally visualize the shape in trame window or in a jupyter kernal using the visualize method.\nsphere.visualize().plot(color=\'magenta\', text=f\'{sphere.name}\')\n```\n\n<p text-align="center"><img src=".\\assets\\sphere.png" alt="Pystl_generated_sphere_stl"></p>\n\n<u>PISTL is an open source project that welcomes contributions from developers from diverse community and backgrounds.\\_</u>\n\ncontact : sumanan047@gmail.com to get added on the project formally.\n',
    'author': 'Suman Saurabh',
    'author_email': 'sumanan047@gmail.com',
    'maintainer': 'Suman Saurabh',
    'maintainer_email': 'sumanan047@gmail.com',
    'url': 'https://github.com/sumanan047/pistl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
