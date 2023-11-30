terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = "eu-west-2"
}

data "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"
}

resource "aws_iam_role" "iam_for_sfn" {
  name = "stepFunctionSampleStepFunctionExecutionIAM"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "states.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "policy_publish_ses" {
  name        = "stepFunctionSampleSESInvocationPolicy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
              "SES:SendEmail"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_policy" "policy_invoke_lambda" {
  name        = "stepFunctionSampleLambdaFunctionInvocationPolicy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction",
                "lambda:InvokeAsync"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

// Attach policy to IAM Role for Step Function
resource "aws_iam_role_policy_attachment" "iam_for_sfn_attach_policy_invoke_lambda" {
  role       = "${aws_iam_role.iam_for_sfn.name}"
  policy_arn = "${aws_iam_policy.policy_invoke_lambda.arn}"
}

resource "aws_iam_role_policy_attachment" "iam_for_sfn_attach_policy_publish_ses" {
  role       = "${aws_iam_role.iam_for_sfn.name}"
  policy_arn = "${aws_iam_policy.policy_publish_ses.arn}"
}

resource "aws_ecs_task_definition" "c9-charliedean-truck-task-definition-t" {
  family                   = "c9-charliedean-truck-task-definition-t"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = "${data.aws_iam_role.ecs_task_execution_role.arn}"
  container_definitions    = <<TASK_DEFINITION
[
  {
    "environment": [
      {"name": "DATABASE_IP", "value": "${var.database_ip}"},
      {"name": "DATABASE_NAME", "value": "${var.database_name}"},
      {"name": "DATABASE_PASSWORD", "value": "${var.database_password}"},
      {"name": "DATABASE_PORT", "value": "${var.database_port}"},
      {"name": "DATABASE_USERNAME", "value": "${var.database_username}"},
      {"name": "AWS_ACCESS_KEY_ID", "value": "${var.aws_access_key_id}"},
      {"name": "AWS_SECRET_ACCESS_KEY", "value": "${var.aws_secret_access_key}"}
    ],
    "name": "c9-charliedean-trucks-t",
    "image": "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-charliedean-trucks-repo:latest",
    "essential": true
  }
]
TASK_DEFINITION

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }
}

resource "aws_ecs_task_definition" "c9-charliedean-dashboard-task-t" {
  family                   = "c9-charliedean-dashboard-task-t"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = "${data.aws_iam_role.ecs_task_execution_role.arn}"
  container_definitions    = <<TASK_DEFINITION
[
  {
    "environment": [
      {"name": "DATABASE_IP", "value": "${var.database_ip}"},
      {"name": "DATABASE_NAME", "value": "${var.database_name}"},
      {"name": "DATABASE_PASSWORD", "value": "${var.database_password}"},
      {"name": "DATABASE_PORT", "value": "${var.database_port}"},
      {"name": "DATABASE_USERNAME", "value": "${var.database_username}"}
    ],
    "name": "c9-charliedean-dashboard-t",
    "image": "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-charliedean-trucks-dashboard:latest",
    "essential": true,
    "portMappings" : [
        {
          "containerPort" : 8501,
          "hostPort"      : 8501
        }
      ]
  }
]
TASK_DEFINITION

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }
}

resource "aws_ecs_service" "c9-charliedean-dashboard-t" {
  name            = "c9-charliedean-dashboard-terraform"
  cluster         = "c9-ecs-cluster"
  task_definition = aws_ecs_task_definition.c9-charliedean-dashboard-task-t.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  force_new_deployment = true 
  depends_on = [aws_ecs_task_definition.c9-charliedean-dashboard-task-t]

network_configuration {
    security_groups = ["sg-0f3b4621265e9db57"]
    subnets         = ["subnet-0d0b16e76e68cf51b","subnet-081c7c419697dec52","subnet-02a00c7be52b00368"]
    assign_public_ip = true
  }
}

resource "aws_lambda_function" "c9-charliedean-lambda-query-t" {
    function_name = "c9-charliedean-lambda-query-t"
    role = "arn:aws:iam::129033205317:role/service-role/c9-charliedean-query-function-role-4oq83pji"
    image_uri = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-charliedean-lambda-query:latest"
    package_type  = "Image"
    environment {
      variables = {
      DATABASE_IP = "${var.database_ip}",
      DATABASE_NAME ="${var.database_name}",
      DATABASE_PASSWORD = "${var.database_password}",
      DATABASE_PORT ="${var.database_port}",
      DATABASE_USERNAME = "${var.database_username}"
    }
}
}

resource "aws_sfn_state_machine" "c9-charliedean-email-report-t" {
  name     = "c9-charliedean-email-report-t"
  role_arn = "${aws_iam_role.iam_for_sfn.arn}"

  definition = <<EOF
{
  "Comment": "A description of my state machine",
  "StartAt": "Lambda Invoke",
  "States": {
    "Lambda Invoke": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "OutputPath": "$.Payload",
      "Parameters": {
        "FunctionName":  "${aws_lambda_function.c9-charliedean-lambda-query-t.arn}"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2
        }
      ],
      "Next": "SendEmail"
    },
    "SendEmail": {
      "Type": "Task",
      "End": true,
      "Parameters": {
        "Content": {
          "Simple": {
            "Body": {
              "Html": {
                "Data.$": "$.body"
              }
            },
            "Subject": {
              "Data": "Daily Report"
            }
          }
        },
        "Destination": {
          "ToAddresses": [
            "trainee.charlie.dean@sigmalabs.co.uk"
          ]
        },
        "FromEmailAddress": "trainee.charlie.dean@sigmalabs.co.uk"
      },
      "Resource": "arn:aws:states:::aws-sdk:sesv2:sendEmail"
    }
  }
}
EOF
}

# Tell the Lambda that the rule/schedule can call it
resource "aws_lambda_permission" "execute-lambda-permission" {
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.c9-charliedean-lambda-query-t.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_scheduler_schedule.c9-charliedean-daily-report-t.arn
}

## Attaching a step function to the schedule ##

# Create a resource that allows running step functions
resource "aws_iam_policy" "step-function-policy" {
    name = "ExecuteStepFunctions_Charlie"
    policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "states:StartExecution"
            ],
            "Resource": [
                aws_sfn_state_machine.c9-charliedean-email-report-t.arn
            ]
        }
    ]
})
}

# Create a role to attach the policy to
resource "aws_iam_role" "iam_for_sfn_2" {
  name = "stepFunctionSampleStepFunctionExecutionIAM_2"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "states.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Principal": {
          "Service": "scheduler.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
      }
    ]
}
EOF
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "attach-execution-policy" {
  role       = aws_iam_role.iam_for_sfn_2.name
  policy_arn = aws_iam_policy.step-function-policy.arn
}

# Create a resource that allows running step functions
resource "aws_iam_policy" "ecs-schedule-permissions" {
    name = "ExecuteECSFunctions"
    policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecs:RunTask"
            ],
            "Resource": [
                aws_ecs_task_definition.c9-charliedean-truck-task-definition-t.arn
            ],
            "Condition": {
                "ArnLike": {
                    "ecs:cluster": "arn:aws:ecs:eu-west-2:129033205317:cluster/c9-ecs-cluster"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": [
                "*"
            ],
            "Condition": {
                "StringLike": {
                    "iam:PassedToService": "ecs-tasks.amazonaws.com"
                }
            }
        }
    ]
})
}


resource "aws_iam_role" "iam_for_ecs" {
  name = "ECSPermissionsForIAM-73sfa"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Principal": {
          "Service": "scheduler.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
      }
    ]
}
EOF
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "attach-ecs-policy" {
  role       = aws_iam_role.iam_for_ecs.name
  policy_arn = aws_iam_policy.ecs-schedule-permissions.arn
}

resource "aws_scheduler_schedule" "c9-charliedean-daily-report-t" {
  name        = "c9-charliedean-daily-report-t"
  group_name  = "default"

  flexible_time_window {
    maximum_window_in_minutes = 15
    mode = "FLEXIBLE"
  }
  schedule_expression_timezone = "Europe/London"
  schedule_expression = "cron(09 13 * * ? *)" 

  target{
    arn = aws_sfn_state_machine.c9-charliedean-email-report-t.arn
    role_arn = aws_iam_role.iam_for_sfn_2.arn
    input = jsonencode({
      Payload = "Hello, ServerlessLand!"
    })
  }
}

resource "aws_scheduler_schedule" "c9-charliedean-trucks-schedule-t" {
  name        = "c9-charliedean-trucks-schedule-t"
  group_name  = "default"

  flexible_time_window {
    maximum_window_in_minutes = 15
    mode = "FLEXIBLE"
  }
  schedule_expression_timezone = "Europe/London"
  schedule_expression = "cron(09 13 * * ? *)" 

  target {
    arn      = "arn:aws:ecs:eu-west-2:129033205317:cluster/c9-ecs-cluster" # arn of the ecs cluster to run on
    # role that allows scheduler to start the task (explained later)
    role_arn = aws_iam_role.iam_for_ecs.arn

    ecs_parameters {
      task_definition_arn = aws_ecs_task_definition.c9-charliedean-truck-task-definition-t.arn
      launch_type         = "FARGATE"

    network_configuration {
        subnets         = ["subnet-0d0b16e76e68cf51b","subnet-081c7c419697dec52","subnet-02a00c7be52b00368"]
        assign_public_ip = true
      }
    }
  }
}