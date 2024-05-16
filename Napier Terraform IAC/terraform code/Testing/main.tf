terraform {
  required_providers {
    aws = {
      source = "/provider.tf"
    }
  }
}

resource "aws_s3_bucket" "npg-ivp-uat-test" {
  bucket = "npg-geneva-dev-test"

  tags = {
    "Application" = "geneva-dev"
    "Stack"       = "dev"
    "Module"      = "geneva"
  }
}

resource "aws_s3_bucket" "npg-ivp-uat-test2" {
  bucket = "npg-geneva-dev-test2"

  tags = {
    "Application" = "geneva-dev"
    "Stack"       = "dev"
    "Module"      = "geneva"
  }
}

resource "aws_s3_bucket" "npg-ivp-uat-test3" {
  bucket = "npg-geneva-dev-test3"

  tags = {
    "Application" = "geneva-dev"
    "Stack"       = "dev"
    "Module"      = "geneva"
  }
}
