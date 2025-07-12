#!/usr/bin/env python3
import boto3
import sys
import os
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv

def load_aws_credentials():
    """Load AWS credentials from .env file"""
    # Load environment variables from .env file
    load_dotenv()
    
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    if not access_key or not secret_key:
        print("Error: AWS_ACCESS_KEY_ID and/or AWS_SECRET_ACCESS_KEY not found in .env file")
        print("Please create a .env file with:")
        print("AWS_ACCESS_KEY_ID=your_access_key")
        print("AWS_SECRET_ACCESS_KEY=your_secret_key")
        sys.exit(1)
    
    # Set environment variables for boto3 to use
    os.environ['AWS_ACCESS_KEY_ID'] = access_key
    os.environ['AWS_SECRET_ACCESS_KEY'] = secret_key
    
    print("AWS credentials loaded from .env file")

def list_s3_files(bucket_name):
    """List all files in the specified S3 bucket"""
    try:
        s3 = boto3.client('s3')
        response = s3.list_objects_v2(Bucket=bucket_name)
        
        if 'Contents' not in response:
            print(f"No files found in bucket '{bucket_name}'")
            return []
        
        files = []
        for obj in response['Contents']:
            files.append({
                'key': obj['Key'],
                'size': obj['Size'],
                'modified': obj['LastModified']
            })
        
        return files
    
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
        print("Make sure your .env file contains valid AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        sys.exit(1)
    except ClientError as e:
        print(f"Error accessing S3: {e}")
        sys.exit(1)

def main():
    # Load AWS credentials from .env file
    load_aws_credentials()
    
    # Prompt user for bucket name
    bucket_name = input("Enter S3 bucket name: ").strip()
    
    if not bucket_name:
        print("Error: Bucket name cannot be empty")
        sys.exit(1)
    
    print(f"\nListing files in S3 bucket: {bucket_name}")
    print("-" * 50)
    
    # Get list of files
    files = list_s3_files(bucket_name)
    
    if not files:
        return
    
    # Display numbered list
    print("\nFiles in bucket:")
    for i, file_info in enumerate(files, 1):
        size_kb = file_info['size'] / 1024
        modified_date = file_info['modified'].strftime('%Y-%m-%d %H:%M:%S')
        print(f"{i:2d}. {file_info['key']} ({size_kb:.1f} KB) - Modified: {modified_date}")
    
    print(f"\nTotal files: {len(files)}")

if __name__ == "__main__":
    main()
