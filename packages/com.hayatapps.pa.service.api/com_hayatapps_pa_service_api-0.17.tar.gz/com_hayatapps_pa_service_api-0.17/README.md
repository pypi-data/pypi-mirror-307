# pa-proto

sudo ln -s $(which python3) /usr/local/bin/python

sudo python3 -m pip install hayatapps_pa_proto-0.1-py3-none-any.whl --break-system-packages

sudo python3 -m pip install -r requirements.txt --break-system-packages

python3 -m grpc_tools.protoc -I proto --python_out=./hayatapps-pa-proto --pyi_out=./hayatapps-pa-proto --grpc_python_out=./hayatapps-pa-proto com/hayatapps/pa/service/model/service.proto


python setup.py sdist bdist_wheel
pip install hayatapps_pa_proto-0.1-py3-none-any.whl
pip install hayatapps_pa_proto-0.1-py3-none-any.whl --force-reinstall

python3 setup.py sdist bdist_wheel
pip3 install dist/hayatapps_paservice_api-0.1-py3-none-any.whl
/Users/user/Library/Python/3.9/bin/twine upload dist/*