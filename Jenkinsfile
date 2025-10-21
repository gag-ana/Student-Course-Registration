pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "gaga730/student-course-registration:latest"
        DOCKER_USER = "gaga730"
        DOCKER_PASS = "gagana2005"
        // Optional: Set KUBECONFIG if needed for remote cluster access
        // KUBECONFIG = "C:\\Users\\hello\\.kube\\config"
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
                kubectl apply -f deployment.yaml --validate=false
                kubectl apply -f service.yaml --validate=false
                kubectl get pods -o wide
                '''
            }
        }
    }

    post {
        success {
            echo 'Docker image built, pushed, and deployed to Kubernetes successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}