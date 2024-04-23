terraform {
  backend "s3" {
    bucket         = "terraform-state-file-global"
    key            = "npg-ivp-uat/terraform.tfstate"
    region         = "us-east-1"
    role_arn       = "arn:aws:iam::381492161742:role/TerraformCrossAccountRole"
    encrypt        = true
  }
}