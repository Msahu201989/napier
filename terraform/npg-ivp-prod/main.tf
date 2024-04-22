resource "aws_s3_bucket" "awswithlinux" {
  #  provider = aws.cross_account
  bucket   = "napiercrossaccount39"

  tags = {
    "Application" = "Geneva_Dev"
    "Stack"       = "DEV"
    "Name"        = "vpc_geneva_dev"
    "Module"      = "Geneva"
  }
}
