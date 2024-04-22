#resource "aws_s3_bucket" "awswithlinux99" {
#  #  provider = aws.cross_account
#  bucket   = "napiercrossaccount39"
#
#  tags = {
#    "Application" = "Geneva_Dev"
#    "Stack"       = "DEV"
#    "Name"        = "vpc_geneva_dev"
#    "Module"      = "Geneva"
#  }
#}


provider "aws" {
  region = "use-east-1"
}

resource "aws_instance" "sample" {
  ami           = "ami-00d48a21603b2119b"
  instance_type = "t3.micro"