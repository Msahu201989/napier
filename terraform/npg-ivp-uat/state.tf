terraform {
  backend "s3" {
    bucket = "ivp-uat-testing"
    key    = "ivp-uat/terraform.tfstate"
    region = "us-east-1"
  }
}

