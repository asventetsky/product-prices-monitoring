import boto3
import os

client = boto3.client("cognito-idp")


def get_user_pool_id():
    response = client.list_user_pools(MaxResults=1)
    return response['UserPools'][0]['Id']


def get_user_pool_client_id(user_pool_id):
    response = client.list_user_pool_clients(
        UserPoolId=user_pool_id,
        MaxResults=1,
    )
    return response['UserPoolClients'][0]['ClientId']


def sign_up(user_pool_client_id):
    response = client.sign_up(
        ClientId=user_pool_client_id,
        Username=os.environ["COGNITO_USER_NAME"],
        Password=os.environ["COGNITO_USER_PASSWORD"],
        UserAttributes=[
            {
                'Name': 'email',
                'Value': os.environ["COGNITO_USER_EMAIL"]
            },
        ],
    )


def main():
    user_pool_id = get_user_pool_id()
    print(f"user_pool_id={user_pool_id}")

    user_pool_client_id = get_user_pool_client_id(user_pool_id)
    print(f"user_pool_client_id={user_pool_client_id}")

    sign_up(user_pool_client_id)

if __name__ == "__main__":
    main()
