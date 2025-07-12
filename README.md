# S3 Bucket Lister

A simple Python script that connects to AWS S3 and lists the contents of a specified bucket, including file names, sizes, and last modified dates.

## Features

- **Secure credential management** - Loads AWS credentials from a local `.env` file
- **Interactive bucket selection** - Prompts user to enter bucket name at runtime
- **Detailed file information** - Shows file name, size (in KB), and last modified timestamp
- **Error handling** - Graceful handling of credential and S3 access errors
- **Clean output** - Numbered list with total file count

## Prerequisites

### Python Dependencies
Install the required Python packages:

```bash
pip install boto3 python-dotenv
```

### AWS Credentials
You'll need an AWS Access Key ID and Secret Access Key with appropriate S3 permissions.

## Setup

### 1. Create Environment File
Create a `.env` file in the same directory as the script:

```env
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_access_key_here
```

**Important Security Notes:**
- Replace the placeholder values with your actual AWS credentials
- Add `.env` to your `.gitignore` file to prevent committing credentials
- Keep the `.env` file secure and never share it publicly

### 2. Configure IAM Permissions
Your AWS user/key needs the following IAM policy attached:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": "arn:aws:s3:::your-bucket-name"
        }
    ]
}
```

Replace `your-bucket-name` with your actual bucket name, or use `*` for access to all buckets.

## Usage

Run the script:

```bash
python s3_browser.py
```

The script will:
1. Load AWS credentials from the `.env` file
2. Prompt you to enter an S3 bucket name
3. Connect to AWS S3 and list all files in the specified bucket
4. Display results with file details and total count

### Example Output

```
AWS credentials loaded from .env file
Enter S3 bucket name: my-documents

Listing files in S3 bucket: my-documents
--------------------------------------------------

Files in bucket:
 1. report-2025.pdf (1456.3 KB) - Modified: 2025-07-10 14:30:22
 2. presentation.pptx (2203.7 KB) - Modified: 2025-07-09 09:15:33
 3. data-export.csv (89.2 KB) - Modified: 2025-07-08 16:45:11
 4. backup/archive.zip (15432.8 KB) - Modified: 2025-07-05 11:20:45

Total files: 4
```

## Error Handling

The script handles common error scenarios:

- **Missing .env file** - Clear instructions on how to create it
- **Invalid AWS credentials** - Helpful error messages
- **Bucket access denied** - IAM permission guidance
- **Bucket doesn't exist** - AWS error details
- **Empty bucket** - Informative message when no files found

## Security Considerations

- **Credential Storage**: AWS credentials are stored locally in `.env` file (not in code)
- **Read-Only Access**: Script only requires `ListBucket` permissions
- **No File Access**: Script cannot download or modify files, only list them
- **Environment Isolation**: Credentials loaded only for script execution

## Troubleshooting

### "AWS credentials not found"
- Verify `.env` file exists in the same directory as the script
- Check that `.env` contains both `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
- Ensure there are no extra spaces or quotes around the values

### "Access Denied" errors
- Verify your AWS credentials are valid and active
- Check that the IAM user/role has the required S3 permissions
- Ensure the bucket name is spelled correctly and exists

### "No files found" message
- Confirm the bucket name is correct
- Verify the bucket actually contains files
- Check if files might be in a different AWS region

## File Structure

```
project-directory/
├── s3_browser.py    # Main script
├── .env             # AWS credentials (create this)
├── README.md        # This documentation
└── .gitignore       # Should include .env
```

