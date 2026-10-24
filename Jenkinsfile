
pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
    }

    environment {
        IMAGE_NAME = 'python-demo-app'
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'echo "GitHub checkout successful"'
                sh 'ls -la'
            }
        }

        stage('Check Python') {
            steps {
                sh '''
                    python3 --version
                    python3 -m pip --version
                '''
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

        stage('Run Unit Tests') {
            steps {
                sh '''
                    .venv/bin/python -m pytest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker image ls ${IMAGE_NAME}
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Tests passed and Docker image was built.'
        }

        failure {
            echo 'FAILED: Check the stage logs to identify the issue.'
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}
