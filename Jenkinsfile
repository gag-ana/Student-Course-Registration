pipeline {
    agent any

    environment {
        // DockerHub
        DOCKER_USER = "gaga730"
        DOCKER_PASS = credentials('docker-hub-password')
        IMAGE_NAME  = "student-course-registration"
        BUILD_TAG   = "${BUILD_NUMBER}"

        // Azure (secured in Jenkins credentials store)
        CLIENT_ID       = credentials('AZ-CLIENT_ID')
        CLIENT_SECRET   = credentials('AZ-CLIENT_SECRET')
        TENANT_ID       = credentials('AZ-TENANT_ID')
        SUBSCRIPTION_ID = "58a5204f-816d-43a8-9730-a61ebdc3fadd"

        // AKS
        RESOURCE_GROUP  = "student-rg"     // ✔ UPDATED
        CLUSTER_NAME    = "student-course-registration-aks"
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
                echo Pushing Docker image...
                echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                docker push %DOCKER_USER%/%IMAGE_NAME%:%BUILD_TAG%
                docker push %DOCKER_USER%/%IMAGE_NAME%:latest
                """
            }
        }

        stage('Azure Login') {
            steps {
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

        stage('Connect to AKS') {
            steps {
                bat """
                echo Fetching AKS credentials...
                az aks get-credentials --resource-group "%RESOURCE_GROUP%" --name "%CLUSTER_NAME%" --overwrite-existing
                """
            }
        }

        stage('Deploy to AKS') {
            steps {
                bat """
                echo Deploying application and Jenkins to AKS...

                kubectl apply -f mysql-deployment.yaml
                kubectl apply -f mysql-service.yaml
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml

                echo Deploying Jenkins...
                kubectl apply -f jenkins-deployment.yaml   // ✔ NEW: Jenkins Deployment
                kubectl apply -f jenkins-service.yaml      // ✔ NEW: Jenkins Service

                echo Checking rollout status...
                kubectl rollout status deployment/student-course-registration-deployment
                kubectl rollout status deployment/jenkins-deployment  // ✔ NEW: Jenkins Deployment Rollout
                kubectl get pods -o wide
                kubectl get svc
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully! App and Jenkins deployed to AKS."
        }
        failure {
            echo "Pipeline failed. Check logs for details."
        }
    }
}
