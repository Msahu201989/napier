# Updated by Mukesh
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "cross_account"
  region = "us-east-1"
  assume_role {
    role_arn = "arn:aws:iam::992382648708:role/TerraformCrossAccountRole"
  }
}



