from setuptools import find_namespace_packages, setup

setup(
    name='sam-djtools',
    long_description_content_type="text/markdown",
    url="https://github.com/humblesami/sam-djtools.git",
    python_requires=">=3",
    setup_requires=['setuptools_scm'],

    include_package_data=True,
    packages=find_namespace_packages(include=["sam_djtools", "sam_djtools.admin_models", "sam_djtools.utils"]),
    package_data={
        "sam_djtools": [
            "navigate_records.py",
            "management/commands/*",
            "templates/admin/change_form.html",
            "static/sam_djtools/change_form_prev_next.js"
        ]
    }
)
