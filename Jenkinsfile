pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "gaga730/student-course-registration:latest"
        KUBECONFIG_PATH = "C:\\Users\\hello\\.kube\\config"
    }

    stages {
        stage('Ensure Minikube is Running') {
            steps {
                bat 'scripts\\ensure_minikube.bat'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
for /f "tokens=*" %%i in ('minikube -p minikube docker-env') do @%%i
docker build -t %DOCKER_IMAGE% .
'''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat '''
                    echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    docker push %DOCKER_IMAGE%
                    '''
                }
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
            echo 'Successfully built, pushed, and deployed to Minikube automatically!'
        }
        failure {
            echo ' Pipeline failed. Check logs for details.'
        }
    }
}