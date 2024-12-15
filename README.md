# Discord Bot 3
This is a discord bot that is integrated with AWS Bedrock using the Titan and Claude models.

## Python Version
- 3.13.1

## Prerequistes
This bot uses AWS Bedrock to utilize LLM models. Enable foundation models in the AWS console.

https://docs.aws.amazon.com/bedrock/latest/userguide/model-access-modify.html

## LLM Models being used
- Claude 3.5 Sonnet
- Claude 3.5 Sonnet v2
- Llama 3.2 90B Instruct
- Titan Text G1 - Lite
- Titan Text G1 - Express

## Create environment variables for:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- DISCORD_TOKEN
- DISCORD_ID

## Running Bot
Running this bot on a container is the preferred approach. 
You will need to do the following to build and run the container.

a. Build Container
```shell
  make build
```

b. Run Container
```shell
  make run-con
```

If you're testing code changes quickly, you can run the code directly on your machine.
This will utilize python on your machine instead of running on a container.
```shell
  make run
```

## Discord Commands
| Command  | options                         | Description                                                                                  |
|:---------|:--------------------------------|:---------------------------------------------------------------------------------------------|
| /ask     | question: string, model: string | Ask an LLM model a question. You can change the default LLM (Titan) by entering model option |
| /models  |                                 | List all of the supported models that can be passed into /ask                                |
| /roll    | sides: integer                  | Roll a dice. Default sides on a dice is 6                                                    |
| /version |                                 | Show bot version                                                                             |