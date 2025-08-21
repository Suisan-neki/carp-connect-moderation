# PowerShell script to attach Bedrock policy to IAM user
# Run this script with AWS CLI configured

param(
    [string]$UserName = "yamas",
    [string]$ProjectName = "carp-connect-moderation"
)

Write-Host "Attaching Bedrock policy to IAM user: $UserName" -ForegroundColor Green

# Get the policy ARN
$PolicyArn = "arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):policy/${ProjectName}-local-development-policy"

Write-Host "Policy ARN: $PolicyArn" -ForegroundColor Yellow

# Attach the policy to the user
try {
    aws iam attach-user-policy --user-name $UserName --policy-arn $PolicyArn
    Write-Host "Successfully attached policy to user: $UserName" -ForegroundColor Green
    
    # Verify the attachment
    Write-Host "Verifying policy attachment..." -ForegroundColor Yellow
    aws iam list-attached-user-policies --user-name $UserName
} catch {
    Write-Host "Error attaching policy: $_" -ForegroundColor Red
    Write-Host "Please ensure:" -ForegroundColor Yellow
    Write-Host "1. AWS CLI is configured with appropriate permissions" -ForegroundColor Yellow
    Write-Host "2. The policy exists in your AWS account" -ForegroundColor Yellow
    Write-Host "3. You have permission to attach policies to users" -ForegroundColor Yellow
}

Write-Host "Script completed." -ForegroundColor Green 