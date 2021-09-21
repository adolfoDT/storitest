<!--
title: 'Stori test'
description: ' This is a simple test for process data in csv and send a notification by email'
layout: Doc
framework: v2
platform: AWS
language: python 3.7
priority: 2
authorLink: 'https://github.com/serverless'
authorName: 'Serverless, inc.'
authorAvatar: 'https://avatars1.githubusercontent.com/u/13742415?s=200&v=4'
-->


# Test architecture
This test is conformed by the services of S3,Lambdas,SES, personally i use CodePipeline to deploy my code using CodeBuild and serverless framework, also i used SQL SERVER to store the data, and DynamoDB as storage layer persistent data for use idempotency

# The process of the Test

The process is executed by inserting a csv file to S3 and it is obtained through a lambda called invokeS3, in that lambda I process the basic data of the csv, to mold a payload in my favor, after processing it I invoke another lambda called idempotency, which as its name indicates is based on that concept, that if for a certain time the event that arrives does not change, the lambda will not be executed unless it changes, for this I use a library called aws_lambda_powertools that was very useful, together with DynamoDB, they create a storage layer persistent, if the payload was accepted, it will send an email with the user's account status


# The csv file
The name of the csv is = {name_user}_{last_name}.csv for example adolfo_diaz.csv, if you create your own csv it will create a new user on de database, with the names that you assigned to the csv



# Local prove

I will give you my AWS account for prove my lambda and see the services, also to do local tests with serverless

-For local test you need to:
1.- Create a virtual enviroment with python
2.- Install serverless
3.- config the aws account with serverless
4.- cd lmds : for execute lambdas
5.- serverless invoke local --function   stori -s dev --aws-profile adolfoAWS 

6.-In the transactions directory you will see a exaple of a csv.


CONSOLE LINK = https://075313463539.signin.aws.amazon.com/console

User name =  AdolfoAdmin

Password = Poropo1994.

AccessKeyId = AKIARDCIIIDZ5PAEAFUA
SecretAccess = 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


# Notes

Right know the email is static, and only i will receive the email, we can update the ses in the review of the test







