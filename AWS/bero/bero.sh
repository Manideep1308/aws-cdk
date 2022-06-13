
echo "activating virtual environment"

source .venv/bin/activate

# echo "do aws configure"

# aws configure


# cdk bootstrap  
cdk bootstrap

# echo "cdk deploy"

cdk deploy $@
