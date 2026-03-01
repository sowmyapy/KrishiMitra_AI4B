# KrishiMitra AWS Infrastructure
# Terraform configuration for production deployment

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket         = "krishimitra-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "ap-south-1"
    encrypt        = true
    dynamodb_table = "krishimitra-terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "KrishiMitra"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"  # Mumbai region for India
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "krishimitra"
}

# VPC Configuration
module "vpc" {
  source = "./modules/vpc"
  
  project_name = var.project_name
  environment  = var.environment
  vpc_cidr     = "10.0.0.0/16"
  
  availability_zones = ["ap-south-1a", "ap-south-1b", "ap-south-1c"]
  public_subnets     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets    = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
  database_subnets   = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]
}

# RDS PostgreSQL with PostGIS
module "rds" {
  source = "./modules/rds"
  
  project_name       = var.project_name
  environment        = var.environment
  vpc_id             = module.vpc.vpc_id
  database_subnets   = module.vpc.database_subnet_ids
  
  instance_class     = "db.t3.medium"
  allocated_storage  = 100
  engine_version     = "15.4"
  
  database_name      = "krishimitra"
  master_username    = "krishimitra_admin"
  
  backup_retention_period = 7
  multi_az               = true
  
  allowed_security_groups = [module.ecs.ecs_security_group_id]
}

# ElastiCache Redis
module "elasticache" {
  source = "./modules/elasticache"
  
  project_name     = var.project_name
  environment      = var.environment
  vpc_id           = module.vpc.vpc_id
  private_subnets  = module.vpc.private_subnet_ids
  
  node_type        = "cache.t3.medium"
  num_cache_nodes  = 2
  engine_version   = "7.0"
  
  allowed_security_groups = [module.ecs.ecs_security_group_id]
}

# Amazon MSK (Managed Kafka)
module "msk" {
  source = "./modules/msk"
  
  project_name    = var.project_name
  environment     = var.environment
  vpc_id          = module.vpc.vpc_id
  private_subnets = module.vpc.private_subnet_ids
  
  kafka_version   = "3.5.1"
  instance_type   = "kafka.t3.small"
  number_of_nodes = 3
  
  allowed_security_groups = [module.ecs.ecs_security_group_id]
}

# S3 Buckets
module "s3" {
  source = "./modules/s3"
  
  project_name = var.project_name
  environment  = var.environment
  
  buckets = {
    satellite = {
      name = "${var.project_name}-satellite-${var.environment}"
      lifecycle_rules = [
        {
          id      = "archive-old-tiles"
          enabled = true
          transition = {
            days          = 90
            storage_class = "GLACIER"
          }
          expiration = {
            days = 365
          }
        }
      ]
    }
    audio = {
      name = "${var.project_name}-audio-${var.environment}"
      lifecycle_rules = [
        {
          id      = "delete-old-recordings"
          enabled = true
          expiration = {
            days = 90
          }
        }
      ]
    }
    models = {
      name = "${var.project_name}-models-${var.environment}"
    }
  }
}

# ECS Fargate for Application
module "ecs" {
  source = "./modules/ecs"
  
  project_name    = var.project_name
  environment     = var.environment
  vpc_id          = module.vpc.vpc_id
  private_subnets = module.vpc.private_subnet_ids
  public_subnets  = module.vpc.public_subnet_ids
  
  # Application container
  container_image = "${aws_ecr_repository.app.repository_url}:latest"
  container_port  = 8000
  cpu             = 1024
  memory          = 2048
  desired_count   = 3
  
  # Auto-scaling
  min_capacity = 2
  max_capacity = 10
  
  # Environment variables
  environment_variables = {
    ENVIRONMENT     = var.environment
    AWS_REGION      = var.aws_region
    DATABASE_URL    = "postgresql://${module.rds.endpoint}/${module.rds.database_name}"
    REDIS_URL       = "redis://${module.elasticache.endpoint}:6379/0"
    KAFKA_BOOTSTRAP_SERVERS = module.msk.bootstrap_brokers
  }
  
  # Secrets from Secrets Manager
  secrets = {
    JWT_SECRET_KEY          = aws_secretsmanager_secret.jwt_secret.arn
    OPENAI_API_KEY          = aws_secretsmanager_secret.openai_key.arn
    TWILIO_ACCOUNT_SID      = aws_secretsmanager_secret.twilio_sid.arn
    TWILIO_AUTH_TOKEN       = aws_secretsmanager_secret.twilio_token.arn
    ELEVENLABS_API_KEY      = aws_secretsmanager_secret.elevenlabs_key.arn
  }
}

# Application Load Balancer
module "alb" {
  source = "./modules/alb"
  
  project_name   = var.project_name
  environment    = var.environment
  vpc_id         = module.vpc.vpc_id
  public_subnets = module.vpc.public_subnet_ids
  
  target_group_arn = module.ecs.target_group_arn
  certificate_arn  = aws_acm_certificate.main.arn
}

# CloudFront CDN
module "cloudfront" {
  source = "./modules/cloudfront"
  
  project_name = var.project_name
  environment  = var.environment
  
  origin_domain_name = module.alb.dns_name
  certificate_arn    = aws_acm_certificate.cloudfront.arn
}

# Lambda Functions for Background Jobs
module "lambda" {
  source = "./modules/lambda"
  
  project_name = var.project_name
  environment  = var.environment
  
  functions = {
    satellite_ingestion = {
      handler     = "handlers.satellite_ingestion.handler"
      runtime     = "python3.11"
      timeout     = 900
      memory_size = 3008
      environment = {
        S3_BUCKET = module.s3.satellite_bucket_name
      }
    }
    
    weather_ingestion = {
      handler     = "handlers.weather_ingestion.handler"
      runtime     = "python3.11"
      timeout     = 300
      memory_size = 1024
    }
    
    stress_prediction = {
      handler     = "handlers.stress_prediction.handler"
      runtime     = "python3.11"
      timeout     = 600
      memory_size = 2048
    }
  }
}

# EventBridge for Scheduled Jobs
resource "aws_cloudwatch_event_rule" "satellite_ingestion" {
  name                = "${var.project_name}-satellite-ingestion"
  description         = "Trigger satellite data ingestion every 3 days"
  schedule_expression = "rate(3 days)"
}

resource "aws_cloudwatch_event_rule" "weather_ingestion" {
  name                = "${var.project_name}-weather-ingestion"
  description         = "Trigger weather data ingestion every 6 hours"
  schedule_expression = "rate(6 hours)"
}

# SageMaker for ML Model Training
module "sagemaker" {
  source = "./modules/sagemaker"
  
  project_name = var.project_name
  environment  = var.environment
  
  notebook_instance_type = "ml.t3.medium"
  training_instance_type = "ml.m5.xlarge"
  
  model_bucket = module.s3.models_bucket_name
}

# Secrets Manager
resource "aws_secretsmanager_secret" "jwt_secret" {
  name = "${var.project_name}/${var.environment}/jwt-secret"
}

resource "aws_secretsmanager_secret" "openai_key" {
  name = "${var.project_name}/${var.environment}/openai-api-key"
}

resource "aws_secretsmanager_secret" "twilio_sid" {
  name = "${var.project_name}/${var.environment}/twilio-sid"
}

resource "aws_secretsmanager_secret" "twilio_token" {
  name = "${var.project_name}/${var.environment}/twilio-token"
}

resource "aws_secretsmanager_secret" "elevenlabs_key" {
  name = "${var.project_name}/${var.environment}/elevenlabs-key"
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "app" {
  name              = "/aws/ecs/${var.project_name}-${var.environment}"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.project_name}-${var.environment}"
  retention_in_days = 14
}

# ECR Repository
resource "aws_ecr_repository" "app" {
  name                 = "${var.project_name}-app"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

# ACM Certificates
resource "aws_acm_certificate" "main" {
  domain_name       = "api.krishimitra.com"
  validation_method = "DNS"
  
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_acm_certificate" "cloudfront" {
  provider          = aws.us-east-1
  domain_name       = "krishimitra.com"
  validation_method = "DNS"
  
  lifecycle {
    create_before_destroy = true
  }
}

# Outputs
output "alb_dns_name" {
  description = "ALB DNS name"
  value       = module.alb.dns_name
}

output "cloudfront_domain" {
  description = "CloudFront distribution domain"
  value       = module.cloudfront.domain_name
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = module.rds.endpoint
  sensitive   = true
}

output "redis_endpoint" {
  description = "Redis endpoint"
  value       = module.elasticache.endpoint
  sensitive   = true
}

output "msk_bootstrap_brokers" {
  description = "MSK bootstrap brokers"
  value       = module.msk.bootstrap_brokers
  sensitive   = true
}

output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.app.repository_url
}
