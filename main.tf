
resource "aws_s3_bucket" "npg-ivp-uat-test" {
  provider = aws.cross_account
  bucket   = "npg-ivp-uat-test34"

  tags = {
    "Application" = "ivp-uat"
    "Stack"       = "uat"
    "Module"      = "ivp"
  }
}
