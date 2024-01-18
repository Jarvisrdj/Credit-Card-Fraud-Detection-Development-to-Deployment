import boto3
import argparse

def main():

    parser = argparse.ArgumentParser(description='Pass model_data, image_uri, endpoint')


    
    parser.add_argument('--model_data', type=str, \
        help='base_model_S3_path'
        )
    parser.add_argument('--image_uri', type=str, \
        help='image URI from ECR'
        )
    parser.add_argument('--model_server_timeout', type=int, \
        help='set up Model server timeout environment variable', \
        default=300
        )
    parser.add_argument('--endpoint', type=str, \
        help='sagemaker endpoint name', \
        default="im"  # inference model
        )
    parser.add_argument('--account_id', type=str, \
        help='AWS account id', \
        )   
    parser.add_argument('--region', type=str, \
        help='AWS region', \
        )   
    parser.add_argument('--s3_path', type=str, \
        help='AWS s3 output path', \
        )  
    
    args = parser.parse_args()

    account_id = args.account_id
    region = args.region
    role = f"arn:aws:iam::{account_id}:role/SagemakerExecution"
    sm_client = boto3.client('sagemaker', region_name=region)

    # Create Model
    im_containers = dict(
            ContainerHostname='im',
            ModelDataUrl=args.model_data,
            Image=args.image_uri,
            Environment={'MODEL_SERVER_TIMEOUT': str(args.model_server_timeout)})


    sm_client.create_model(
        ModelName = args.endpoint + '-model',
        ExecutionRoleArn = role,
        PrimaryContainer = im_containers)

    # Create Endpoint Config
    sm_client.create_endpoint_config(
        EndpointConfigName = args.endpoint + "-config",
        ProductionVariants = [
            {
                "VariantName": "im",
                "ModelName": args.endpoint + '-model',
                "InitialInstanceCount": 1,
                "InstanceType": "ml.t2.medium",
            }
        ],
        AsyncInferenceConfig={
            "OutputConfig": {
                # Location to upload response outputs when no location is provided in the request.
                "S3OutputPath": args.path,
                # (Optional) specify Amazon SNS topics
            },
            "ClientConfig": {
                # (Optional) Specify the max number of inflight invocations per instance
                # If no value is provided, Amazon SageMaker will choose an optimal value for you
                "MaxConcurrentInvocationsPerInstance": 4
            }
        }
    )

    # Create Endpoint
    sm_client.create_endpoint(EndpointName=args.endpoint, 
                            EndpointConfigName=args.endpoint + '-config') 


if __name__ == '__main__':
    main()