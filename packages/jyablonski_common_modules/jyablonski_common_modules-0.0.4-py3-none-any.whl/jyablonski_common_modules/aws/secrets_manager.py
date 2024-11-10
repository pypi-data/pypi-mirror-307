import botocore


def get_secret_value(client: botocore.client, secret: str) -> str:
    """
    Function to grab a Secret from AWS Secrets Manager

    Args:
        client (botocore.Client): S3 Secrets Manager Client

        secret (str): The Name of the Secret in Secrets Manager

    Returns:
        The Requested Secret Value
    """
    try:
        creds = client.get_secret_value(SecretId=secret)["SecretString"]

        return creds
    except BaseException as e:
        raise e(f"Error Occurred while grabbing secret {secret}, {e}")
