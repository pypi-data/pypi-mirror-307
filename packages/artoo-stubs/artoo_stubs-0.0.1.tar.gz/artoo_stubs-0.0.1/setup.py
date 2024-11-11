from distutils.core import setup

setup(
    name="artoo-stubs",
    version="0.0.1",
    packages=["awsglue-stubs", "pyspark-stubs"],
    package_data={
      "awsglue-stubs": ["py.typed", "*.pyi", "*/*.pyi"],
      "pyspark-stubs": ["py.typed", "*.pyi", "*/*.pyi"],
    },
)
