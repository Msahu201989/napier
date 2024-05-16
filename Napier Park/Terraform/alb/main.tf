provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "shared_dev_vpc" {
  cidr_block       = "172.18.83.0/26"
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    "Application" = "Control-M|Alfresco"
    "Stack"       = "DEV"
    "Name"        = "vpc_shared_dev"
    "Module"      = "Shared"
  }
}

resource "aws_subnet" "private_subnet_az1" {
  vpc_id                  = aws_vpc.shared_dev_vpc.id
  cidr_block              = "172.18.83.0/27"
  availability_zone       = "us-east-1a"  // Specify the availability zone, not the ID
  map_public_ip_on_launch = false

  tags = {
    "Stack"       = "Shared"
    "Module"      = "VPC"
    "Name"        = "vpc_shared_dev_pvt_az1"
    "Application" = "Control-M|Alfresco"
  }
}

resource "aws_subnet" "private_subnet_az2" {
  vpc_id                  = aws_vpc.shared_dev_vpc.id
  cidr_block              = "172.18.83.32/27"
  availability_zone       = "us-east-1b"  // Specify the availability zone, not the ID
  map_public_ip_on_launch = false

  tags = {
    "Stack"       = "Shared"
    "Module"      = "VPC"
    "Name"        = "vpc_shared_dev_pvt_az2"
    "Application" = "Control-M|Alfresco"
  }
}

resource "aws_security_group" "alb_sg" {
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

resource "aws_lb" "alb_shared_dev" {
  name               = "alb-shared-dev"
  internal           = true
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [
    aws_subnet.private_subnet_az1.id,
    aws_subnet.private_subnet_az2.id,
  ]

  enable_deletion_protection = false

  tags = {
    "Module"      = "Load Balancer"
    "Application" = "Alfresco"
    "Stack"       = "DEV"
  }
}

resource "aws_lb_target_group" "alfresco_transform_router_tg" {
  name               = "Alfresco-Transform-Router-Dev-tg"
  port               = 8095
  protocol           = "HTTP"
  target_type        = "ip"
  vpc_id             = aws_vpc.shared_dev_vpc.id
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

  tags = {}
}

resource "aws_lb_target_group" "alfresco_transform_core_tg" {
  name               = "Alfresco-Transform-Core-Dev"
  port               = 8090
  protocol           = "HTTP"
  target_type        = "ip"
  vpc_id             = aws_vpc.shared_dev_vpc.id
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

  tags = {}
}

resource "aws_lb_listener" "app_listener_8095" {
  load_balancer_arn = aws_lb.alb_shared_dev.arn
  port              = 8095
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.alfresco_transform_router_tg.arn
  }
}

#resource "aws_lb_listener" "app_listener_80" {
#  load_balancer_arn = aws_lb.alb_shared_dev.arn
#  port              = 80
#  protocol          = "HTTP"
#
#  default_action {
#    type = "redirect"
#
#    redirect {
#      protocol    = "HTTPS"
#      port        = "443"
#      status_code = "HTTP_301"
#    }
#  }
#}

resource "aws_lb_listener" "app_listener_8099" {
  load_balancer_arn = aws_lb.alb_shared_dev.arn
  port              = 8099
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.alfresco_transform_core_tg.arn
  }
}

#resource "aws_lb_listener" "app_listener_443" {
#  load_balancer_arn = aws_lb.alb_shared_dev.arn
#  port              = 443
#  protocol          = "HTTPS"
#
#  default_action {
#    type             = "fixed-response"
#
#    fixed_response {
#      content_type = "text/html"
#      message_body = "<h1>Error 503</h1> <p>This path is not configured in the listener rules</p> <p> - Shared Dev ALB</p>"
#      status_code  = "503"
#    }
#  }
#}
