pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "gaga730/student-course-registration:latest"
        DOCKER_USER = "gaga730"
        DOCKER_PASS = "gagana2005"

        // Path to your Kubernetes kubeconfig file
        KUBECONFIG_PATH = "C:\\Users\\hello\\.kube\\config"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                bat "docker build -t %DOCKER_IMAGE% ."
            }
        }

        stage('Push Docker Image') {
            steps {
                bat '''
                echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                docker push %DOCKER_IMAGE%
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                set KUBECONFIG=%KUBECONFIG_PATH%
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml
                kubectl get pods -o wide
                '''
            }
        }
    }

    post {
        success {
            echo ' Docker image built, pushed, and deployed to Kubernetes successfully!'
        }
        failure {
            echo ' Pipeline failed. Check logs for details.'
        }
    }
}