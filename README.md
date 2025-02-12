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
git remote add origin https://$GITHUB_TOKEN@github.com/jesvin1/mlops.git




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

## ETL assets
git checkout -b etl
cd etl/
git add . &&\
git commit -m "initial commit of etl assets" &&\
git push --set-upstream origin etl
cd ..
## Training Assets
git checkout -b model
```
- Modify the `trainingjob.json` as follows:
    - *Replace Account id with respective Account id*
    - *Replace region with `us-east-1` 
```
sed -i "s/<AccountId>/${AWS_ACCOUNT_ID}/" model/trainingjob.json
sed -i "s/<Region>/${AWS_DEFAULT_REGION}/" model/trainingjob.json

## create a new service role for Sagemaker with name as `MLOps`

cd model/
- push the code to master branch
```
git add . &&\
git commit -m "Initial commit of model assets" &&\
git push --set-upstream origin model
git checkout -b feature-branch
git push origin feature-branch

```