pipeline {
    agent any

    environment {
        DOCKER_USER = "gaga730"
        DOCKER_PASS = "gagana2005"
        IMAGE_NAME  = "student-course-registration"
        BUILD_TAG   = "${BUILD_NUMBER}"
        KUBECONFIG_PATH = "C:\\Users\\hello\\.kube\\config"  // Will be replaced with AKS kubeconfig
        RESOURCE_GROUP = "Student-course-Registration-rg"
        CLUSTER_NAME = "student-course-registration-aks"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                bat """
                echo Building Docker image...
                docker build -t %DOCKER_USER%/%IMAGE_NAME%:%BUILD_TAG% .
                docker tag %DOCKER_USER%/%IMAGE_NAME%:%BUILD_TAG% %DOCKER_USER%/%IMAGE_NAME%:latest
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                bat """
                echo Pushing image to Docker Hub...
                echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                docker push %DOCKER_USER%/%IMAGE_NAME%:%BUILD_TAG%
                docker push %DOCKER_USER%/%IMAGE_NAME%:latest
                """
            }
        }

        stage('Connect to AKS') {
            steps {
                bat """
                echo Fetching AKS credentials...
                az aks get-credentials --resource-group %RESOURCE_GROUP% --name %CLUSTER_NAME% --overwrite-existing
                """
            }
        }

        stage('Deploy to AKS') {
            steps {
                bat """
                echo Deploying to Azure AKS cluster...
                set KUBECONFIG=%USERPROFILE%\\.kube\\config

                REM Update image in deployment
                kubectl set image deployment/student-course-registration-deployment student-course-registration=%DOCKER_USER%/%IMAGE_NAME%:%BUILD_TAG%

                REM Apply database and app configurations
                kubectl apply -f mysql-deployment.yaml
                kubectl apply -f mysql-service.yaml
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml

                REM Wait for rollout to complete
                kubectl rollout status deployment/student-course-registration-deployment

                REM Show pod and service status
                kubectl get pods -o wide
                kubectl get svc
                """
            }
        }
    }

    post {
        success {
            echo "CI/CD pipeline completed successfully! Your app is now live on Azure AKS."
        }
        failure {
            echo "Pipeline failed. Check Jenkins logs for details."
        }
    }
}