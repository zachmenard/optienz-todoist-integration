from setuptools import setup

setup(name='todoist_integrations',
      version='0.1',
      description='OptiEnz ToDoist Integrations',
      url='',
      author='Zachary Menard',
      author_email='zach.menard@optienz.com',
      license='MIT',
      packages=['todoist_integrations'],
	  install_requires=['xlrd', 'todoist-python'],
      zip_safe=False)