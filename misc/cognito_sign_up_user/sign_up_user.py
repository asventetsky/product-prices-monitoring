import boto3
import os

client = boto3.client("cognito-idp")


def build_user():
    return {
        "name": os.environ["COGNITO_USER_NAME"],
        "password": os.environ["COGNITO_USER_PASSWORD"],
        "email": os.environ["COGNITO_USER_EMAIL"]
    }


def get_user_pool_id():
    response = client.list_user_pools(MaxResults=1)
    return response['UserPools'][0]['Id']


def get_user_pool_client_id(user_pool_id):
    response = client.list_user_pool_clients(
        UserPoolId=user_pool_id,
        MaxResults=1,
    )
    return response['UserPoolClients'][0]['ClientId']


def sign_up(user_pool_client_id, user):
    client.sign_up(
        ClientId=user_pool_client_id,
        Username=user["name"],
        Password=user["password"],
        UserAttributes=[
            {
                'Name': 'email',
                'Value': user["email"]
            },
        ],
    )


def main():
    user = build_user()
    print(f"Signing up `{user['name']}`")
    user_pool_id = get_user_pool_id()
    user_pool_client_id = get_user_pool_client_id(user_pool_id)
    sign_up(user_pool_client_id, user)

    print(f"Finished signing up `{user['name']}`")

if __name__ == "__main__":
    main()
