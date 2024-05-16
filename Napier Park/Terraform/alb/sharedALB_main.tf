

resource "aws_vpc" "shared_uat_vpc" {
  cidr_block           = "172.18.83.64/26"
  instance_tenancy     = "default"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    "Name"        = "vpc_shared_uat"
    "Module"      = "Shared"
    "Application" = "Control-M|Alfresco"
    "Stack"       = "UAT"
  }
}

resource "aws_subnet" "uat_subnet_az1" {
  vpc_id                  = aws_vpc.shared_uat_vpc.id
  cidr_block              = "172.18.83.64/27"
  map_public_ip_on_launch = false
  availability_zone       = "us-east-1a"
  tags = {
    "Name"        = "vpc_shared_uat_pvt_az1"
    "Module"      = "VPC"
    "Application" = "Control-M|Alfresco"
    "Stack"       = "Shared"
  }
}

resource "aws_subnet" "uat_subnet_az2" {
  vpc_id                  = aws_vpc.shared_uat_vpc.id
  cidr_block              = "172.18.83.96/27"
  map_public_ip_on_launch = false
  availability_zone       = "us-east-1b"
  tags = {
    "Name"        = "vpc_shared_uat_pvt_az2"
    "Module"      = "VPC"
    "Application" = "Control-M|Alfresco"
    "Stack"       = "Shared"
  }
}

resource "aws_security_group" "example_sg" {
  name        = "example"
  description = "Allow inbound traffic"
  vpc_id      = aws_vpc.shared_uat_vpc.id

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "uat_loadbalancer" {
  name               = "alb-shared-uat"
  internal           = true
  load_balancer_type = "application"
  security_groups    = [aws_security_group.example_sg.id]
  subnets            = [
    aws_subnet.uat_subnet_az1.id,
    aws_subnet.uat_subnet_az2.id,
  ]
  tags = {
    "Module"      = "Load Balancer"
    "Application" = "Alfresco"
    "Stack"       = "UAT"
  }
}

resource "aws_lb_listener" "uat_listener_443" {
  load_balancer_arn = aws_lb.uat_loadbalancer.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"

  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/html"
      status_code  = "503"
      message_body = "<h1>Error 503</h1> <p>This path is not configured in the listener rules</p> <p> - Shared UAT ALB</p>"
    }
  }

  certificate_arn = "arn:aws:acm:us-east-1:719927028882:certificate/fb1332d4-01e5-41b5-abac-bb3516cfb924"
}

resource "aws_lb_listener" "uat_listener_8099" {
  load_balancer_arn = aws_lb.uat_loadbalancer.arn
  port              = 8099
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.uat_targetgroup_core.arn
  }
}

resource "aws_vpc" "shared_dev_vpc" {
  cidr_block           = "172.18.83.0/26"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    "Application" = "Control-M|Alfresco"
    "Stack"       = "DEV"
    "Name"        = "vpc_shared_dev"
    "Module"      = "Shared"
  }
}

resource "aws_subnet" "dev_subnet_az1" {
  vpc_id                  = aws_vpc.shared_dev_vpc.id
  cidr_block              = "172.18.83.0/27"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = false
  tags = {
    "Stack"       = "Shared"
    "Module"      = "VPC"
    "Name"        = "vpc_shared_dev_pvt_az1"
    "Application" = "Control-M|Alfresco"
  }
}

resource "aws_subnet" "dev_subnet_az2" {
  vpc_id                  = aws_vpc.shared_dev_vpc.id
  cidr_block              = "172.18.83.32/27"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = false
  tags = {
    "Stack"       = "Shared"
    "Module"      = "VPC"
    "Name"        = "vpc_shared_dev_pvt_az2"
    "Application" = "Control-M|Alfresco"
  }
}

resource "aws_security_group" "alb_dev_sg" {
  name        = "alb_sg"
  description = "Security group for ALB"
  vpc_id      = aws_vpc.shared_dev_vpc.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "dev_loadbalancer" {
  name               = "alb-shared-dev"
  internal           = true
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_dev_sg.id]
  subnets            = [
    aws_subnet.dev_subnet_az1.id,
    aws_subnet.dev_subnet_az2.id,
  ]
  enable_deletion_protection = false
  tags = {
    "Module"      = "Load Balancer"
    "Application" = "Alfresco"
    "Stack"       = "DEV"
  }
}

resource "aws_lb_target_group" "uat_targetgroup_core" {
  name       = "alfresco-transform-core-tg" // Modified name to comply with naming conventions
  port       = 8099
  protocol   = "HTTP"
  target_type = "ip"
  vpc_id     = aws_vpc.shared_uat_vpc.id
  health_check {
    interval            = 30
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    healthy_threshold   = 5
    unhealthy_threshold = 2
    matcher             = "200"
    path                = "/"
  }
}

resource "aws_lb_target_group" "dev_targetgroup_router" {
  name       = "Alfresco-Transform-Router-Dev-tg"
  port       = 8095
  protocol   = "HTTP"
  target_type = "ip"
  vpc_id     = aws_vpc.shared_dev_vpc.id
  health_check {
    interval            = 30
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    healthy_threshold   = 5
    unhealthy_threshold = 2
    matcher             = "200"
    path                = "/"
  }
}

resource "aws_lb_target_group" "dev_targetgroup_core" {
  name       = "Alfresco-Transform-Core-Dev"
  port       = 8090
  protocol   = "HTTP"
  target_type = "ip"
  vpc_id     = aws_vpc.shared_dev_vpc.id
  health_check {
    interval            = 30
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    healthy_threshold   = 5
    unhealthy_threshold = 2
    matcher             = "200"
    path                = "/"
  }
}

resource "aws_lb_listener" "dev_listener_8095" {
  load_balancer_arn = aws_lb.dev_loadbalancer.arn
  port              = 8095
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.dev_targetgroup_router.arn
  }
}

resource "aws_lb_listener" "dev_listener_8099" {
  load_balancer_arn = aws_lb.dev_loadbalancer.arn
  port              = 8099
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.dev_targetgroup_core.arn
  }
}


output "shared_uat_vpc" {
  value = "shared_uat_vpc"
}

output "load_balancer" {
  value = "uat_loadbalancer"
}
