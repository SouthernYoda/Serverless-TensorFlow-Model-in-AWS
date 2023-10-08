# Serverless TensorFlow Model in AWS

This is a complementary repository to a Median article describing the code used in this repository. Each directory is associated with the appropriate article in this two part series. 

In this repository you will find a code example of training a Binary Classification Model and optimizing it for a dataset that is skewed. Afterwards using the AWS SAM framework we will deploy a lambda function that will be able to take the trained model and generate predictions.

Primary Features:
- Model accounts for skew in training data
- Models can be quickly changed out without redeploying the lambda function
- Build a container lambda image for hosting in Lambda

Articles:
1. [Training and Optimizing a Binary Classification Model](https://medium.com/p/f6ebe032c258)
2. [Deploying a Trained TensorFlow Model to AWS Lambda](https://medium.com/p/f3d356fd5208)