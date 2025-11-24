import os
import json

STAGE = os.environ["STAGE"]

# running in deployed Lambda
if STAGE in ("dev", "prod"):
    import boto3

    client = boto3.client(
        "secretsmanager",
        region_name=os.environ["AWS_REGION"],
    )
    secret_value = client.get_secret_value(SecretId=os.environ["DATABASE_SECRET_NAME"])
    secret = json.loads(secret_value["SecretString"])

    os.environ["DATABASE_URL"] = secret["DATABASE_URL"]
else:
    # running locally / tests
    from dotenv import load_dotenv

    load_dotenv()


DATABASE_URL = os.environ["DATABASE_URL"]
MAX_USER_CREATED_REQUESTS = os.environ["MAX_USER_CREATED_REQUESTS"]
MAX_USER_CREATED_FAVORITES = os.environ["MAX_USER_CREATED_FAVORITES"]
