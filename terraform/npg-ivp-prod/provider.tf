#provider "aws" {
#  region = "us-east-1"
#}
#
#provider "aws" {
#  alias  = "cross_account"
#  region = "us-east-1"
#  assume_role {
#    role_arn = "arn:aws:iam::851725296471:role/TerraformCrossAccountRole"
#  }
#}
#
provider "aws" {
  alias  = "cross_account"
  region = "us-east-1"
  assume_role {
    role_arn = "arn:aws:iam::851725296471:role/TerraformCrossAccountRole"
  }
}

# Set default provider for aws_vpc and aws_subnet to the cross-account provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }

  providers {
    aws = aws.cross_account
  }
}
