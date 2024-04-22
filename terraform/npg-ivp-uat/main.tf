provider "aws" {
  region = "us-east-1"  # Replace this with your desired AWS region
}

resource "aws_s3_bucket" "awswithlinux99" {
  bucket = "napiercrossaccount39"

  tags = {
    "Application" = "Geneva_Dev"
    "Stack"       = "DEV"
    "Name"        = "vpc_geneva_dev"
    "Module"      = "Geneva"
  }
}
