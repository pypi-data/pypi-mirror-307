**Make PIP your self**

1. `git clone https://github.com/humblesami/pytils.git`
2. `cd pytils`
3. Find and replace `sam_pytools` with your own `your_module_name`
4. Put the code of app in folder root/your_module_name

**Build and test using sample_usage locally**

rm -r dist/*

rm -r build/*

install python

create your virtual environment

activate the virtual environment

`pip install --use-pep517 -r requirements.txt`

`python -m build`

**Test your just built package before upload**

`pip uninstall -y your_module_name`

`pip install dist/sam_djtools-1.2.42-py3-none-any.whl`

**Upload your pip**

Install twine

`sudo apt-get update`

`sudo apt-get install twine`

https://twine.readthedocs.io/en/stable/

`pip install twine`

**Sample config files for twine**

1. .pypirc_test (add this to root directory where setup.py exists)
```
[distutils]
  index-servers = testpypi

[testpypi]
  repository = https://test.pypi.org/legacy/
  username = __token__
  password = xxx
```
To obtain an api token, you have to sign in and open
https://test.pypi.org/manage/account/#api-tokens

2. .pypirc_prod (add this to root directory where setup.py exists)
```
[distutils]
  index-servers = pypi

[pypi]
  repository = https://upload.pypi.org/legacy/
  username = __token__
  password = your_api_token
```
To obtain an api token, you have to sign in and open
https://pypi.org/manage/account/#api-tokens


**Test Upload**

`twine upload --repository testpypi dist/*`

`twine upload dist/*`

*After upload Install the uploaded package*

**Install and test the uploaded package**

    pip uninstall your_module_name

    pip install -i https://test.pypi.org/simple/ your_module_name

**Final Step, Upload to Production**

`twine upload dist/*`

*After upload Install the uploaded package*

pip install your_module_name

use as

    from your_module_name import SomeClassOrMethod
    from your_module_name.sub_folder_name.filename import SomeClassOrMethod
