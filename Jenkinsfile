
pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
    }

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPOSITORY = 'devops-ecr-practice'
        AWS_ACCOUNT_ID = '824939473621'
        IMAGE_NAME = 'python-demo-app'
        IMAGE_TAG = "${BUILD_NUMBER}"
        ECR_REGISTRY = '824939473621.dkr.ecr.us-east-1.amazonaws.com'
        ECR_IMAGE = '824939473621.dkr.ecr.us-east-1.amazonaws.com/devops-ecr-practice'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'echo "Source checkout successful"'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '.venv/bin/python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${ECR_IMAGE}:${IMAGE_TAG}
                '''
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region ${AWS_REGION} \
                      | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                '''
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh '''
                    docker push ${ECR_IMAGE}:${IMAGE_TAG}
                    echo "Image pushed: ${ECR_IMAGE}:${IMAGE_TAG}"
                '''
            }
        }

        stage('Verify Image in ECR') {
            steps {
                sh '''
                    aws ecr describe-images \
                      --repository-name ${ECR_REPOSITORY} \
                      --image-ids imageTag=${IMAGE_TAG} \
                      --region ${AWS_REGION}
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Tests passed, Docker image built and pushed to ECR.'
        }
        failure {
            echo 'FAILED: Check Console Output for the failing stage.'
        }
        always {
            echo 'Pipeline execution completed.'
        }
    }
}
