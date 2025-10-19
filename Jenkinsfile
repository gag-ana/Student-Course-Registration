pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "gaga730/student-course-registration:latest"
        DOCKER_USER = "gaga730"
        DOCKER_PASS = "gagana2005"

        // Path to your Minikube kubeconfig file
        KUBECONFIG_PATH = "C:\\Users\\hello\\.kube\\config"
    }

    stages {
        stage('Start Minikube') {
            steps {
                bat '''
                echo Checking Minikube status...
                minikube status
                if %ERRORLEVEL% NEQ 0 (
                    echo Starting Minikube...
                    minikube start
                ) else (
                    echo Minikube is already running.
                )

                echo Waiting for Minikube to be ready...
                for /l %%x in (1, 1, 30) do (
                    kubectl get nodes >nul 2>&1
                    if %ERRORLEVEL% EQU 0 (
                        echo Minikube is ready.
                        goto :done
                    )
                    echo Waiting... %%x
                    timeout /t 5 >nul
                )
                :done
                '''
            }
        }

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

        stage('Deploy to Kubernetes (Minikube)') {
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
            echo 'Docker image built, pushed, and deployed to Minikube successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}