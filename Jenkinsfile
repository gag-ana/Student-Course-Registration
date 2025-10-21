pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "gaga730/student-course-registration:latest"
        DOCKER_USER = "gaga730"
        DOCKER_PASS = "gagana2005"
        KUBECONFIG_PATH = "C:\\Users\\hello\\.kube\\config"
    }

    stages {

        stage('Ensure Minikube is Running') {
            steps {
                bat '''
echo Checking Minikube status...

REM Check if Minikube is running
minikube status >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Minikube not running. Starting Minikube automatically...
    minikube start --driver=docker

    echo Waiting for Minikube to be ready...
    setlocal enabledelayedexpansion
    set COUNT=1
:waitLoop
    kubectl get nodes >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo  Minikube is ready!
        goto :done
    )
    echo Waiting... !COUNT!
    set /a COUNT+=1
    if !COUNT! LEQ 30 (
        timeout /t 5 >nul
        goto :waitLoop
    )
    echo  ERROR: Minikube did not become ready in time.
    exit /b 1
:done
) else (
    echo Minikube is already running.
)

echo Setting Docker environment to Minikube...
for /f "tokens=*" %%i in ('minikube -p minikube docker-env') do @%%i
'''
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
            echo ' Successfully built, pushed, and deployed to Minikube automatically!'
        }
        failure {
            echo ' Pipeline failed. Check logs for details.'
        }
    }
}