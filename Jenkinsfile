pipeline {
    agent any

    environment {
        // DockerHub credentials
        DOCKER_USER = "gaga730"
        IMAGE_NAME  = "student-course-registration"
        BUILD_TAG   = "${BUILD_NUMBER}"

        // Azure configuration
        CLIENT_ID       = "ab3b9833-48e2-4a0b-a1f3-0914de8689f5"
        TENANT_ID       = "7b887c76-d8d8-4448-9bf5-a51820345eb4"
        SUBSCRIPTION_ID = "58a5204f-816d-43a8-9730-a61ebdc3fadd"

        // AKS details
        RESOURCE_GROUP  = "Student-course-Registration-rg"
        CLUSTER_NAME    = "student-course-registration-aks"
        DEPLOYMENT_NAME = "student-course-registration"
        CONTAINER_NAME  = "student-course-registration-container"
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
                withCredentials([string(credentialsId: 'DOCKER_PASSWORD', variable: 'DOCKER_PASS')]) {
                    bat """
                    echo Logging into Docker Hub...
                    echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    docker push %DOCKER_USER%/%IMAGE_NAME%:%BUILD_TAG%
                    docker push %DOCKER_USER%/%IMAGE_NAME%:latest
                    """
                }
            }
        }

        stage('Login to Azure') {
            steps {
                withCredentials([string(credentialsId: 'AZ-CLIENT_SECRET', variable: 'CLIENT_SECRET')]) {
                    bat """
                    echo Logging into Azure...
                    az login --service-principal ^
                        -u %CLIENT_ID% ^
                        -p %CLIENT_SECRET% ^
                        --tenant %TENANT_ID%

                    az account set --subscription %SUBSCRIPTION_ID%
                    """
                }
            }
        }

        stage('Connect to AKS') {
            steps {
                bat """
                echo Fetching AKS credentials...
                az aks get-credentials --resource-group "%RESOURCE_GROUP%" --name "%CLUSTER_NAME%" --overwrite-existing
                """
            }
        }

        stage('Update AKS Deployment') {
            steps {
                bat """
                echo Updating AKS deployment with new image...
                kubectl set image deployment/%DEPLOYMENT_NAME% %CONTAINER_NAME%=%DOCKER_USER%/%IMAGE_NAME%:%BUILD_TAG%
                kubectl rollout status deployment/%DEPLOYMENT_NAME%
                kubectl get pods -o wide
                kubectl get svc
                """
            }
        }
    }

    post {
        success {
            echo " CI/CD pipeline completed successfully! Your app is now live on Azure AKS."
        }
        failure {
            echo " Pipeline failed. Check Jenkins logs for details."
        }
    }
}