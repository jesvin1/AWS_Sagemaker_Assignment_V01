## Create a README.md file
## Initializin the git 
 git init
## Create a .gitignore file
## Create a .env file
## Create a requirement.txt

## Creating the virtual env for the folder 

 python3 -m venv .sagemmakerv01
 source .sagemmakerv01/bin/activate
 python3 -m pip install -r requirements.txt

## Create github repository
export $(grep -v '^#' .env | xargs)
echo $GITHUB_TOKEN
git init
git add .
git commit -m "first commit"
git branch -M main

git remote add origin https://$GITHUB_TOKEN@github.com/jesvin1/AWS_Sagemaker_Assignment_V01.git
git push -u origin main


## Setting up the default AWS variables
export AWS_DEFAULT_REGION=$(aws configure get region)
echo $AWS_DEFAULT_REGION
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
echo $AWS_ACCOUNT_ID
export DATA_BUCKET="data-${AWS_DEFAULT_REGION}-${AWS_ACCOUNT_ID}"
export PIPELINE_BUCKET="mlops-${AWS_DEFAULT_REGION}-${AWS_ACCOUNT_ID}"

echo "export AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION" >> ~/.bashrc
echo "export DATA_BUCKET=$DATA_BUCKET" >> ~/.bashrc
echo "export PIPELINE_BUCKET=$PIPELINE_BUCKET" >> ~/.bashrc

## Create S3 Bucket for Storage of dataset

aws s3 mb "s3://${DATA_BUCKET}" --region $AWS_DEFAULT_REGION
## Enable the versioning
aws s3api put-bucket-versioning --bucket "${DATA_BUCKET}" --versioning-configuration Status=Enabled --region $AWS_DEFAULT_REGION
## Download the dataset 
wget /data https://raw.githubusercontent.com/manifoldailearning/mlops-with-aws-datascientists/main/Section-16-mlops-pipeline/dataset/abalone.csv
mv abalone.csv ./data/

## Create S3 Bucket for Storage of output of Feature Engineering

aws s3 mb "s3://${PIPELINE_BUCKET}" --region $AWS_DEFAULT_REGION 
aws s3api put-bucket-versioning --bucket "${PIPELINE_BUCKET}" --versioning-configuration Status=Enabled --region $AWS_DEFAULT_REGION

## Create Container Image Repository in Elastic Container Registry
- Create a Private Repository with repo name as `abalone`


## Training Assets
```
- Modify the `trainingjob.json` as follows:
    - *Replace Account id with respective Account id*
    - *Replace region with `us-east-1` 
```
sed -i "s/<AccountId>/${AWS_ACCOUNT_ID}/" model/trainingjob.json
sed -i "s/<Region>/${AWS_DEFAULT_REGION}/" model/trainingjob.json

## Create Docker Container - Train & Test
```
cd model/
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin 763104351884.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com

docker build --build-arg REGION=$AWS_DEFAULT_REGION -f Dockerfile -t tf_model:1.0 .
```
## For Unit testing
```
cd ..
cd tests/unit_test/
mkdir -p model && \
mkdir -p output
docker run --rm --name 'my_model' \
    -v "$PWD/model:/opt/ml/model" \
    -v "$PWD/output:/opt/ml/output" \
    -v "$PWD/input:/opt/ml/input" tf_model:1.0 train
```
## Test of Prediction
- Prediction
```
docker run --rm --name 'my_model' \
-v "$PWD/model:/opt/ml/model" \
-v "$PWD/output:/opt/ml/output" \
-v "$PWD/input:/opt/ml/input" tf_model:1.0 test \
"[[4.400000000000000022e-01,3.449999999999999734e-01,1.000000000000000056e-01,3.659999999999999920e-01,1.219999999999999973e-01,9.049999999999999711e-02,1.199999999999999956e-01,0.000000000000000000e+00,1.000000000000000000e+00,0.000000000000000000e+00]]"
```

## Serve on Port:8080
```
docker run --rm --name 'my_model' \
    -p 8080:8080 \
    -v "$PWD/model:/opt/ml/model" \
    -v "$PWD/output:/opt/ml/output" \
    -v "$PWD/input:/opt/ml/input" tf_model:1.0 serve

```

## Test the API
```
change the directory in new terminal to unit_test
python3 app_test.py

- Modify threshold value
```
 cd ..
 cd system_test/
sed -i "s/<Threshold>/3.1/" ./buildspec.yml
```

