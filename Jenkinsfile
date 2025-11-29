pipeline {
    agent any

    environment {
        // DockerHub
        DOCKER_USER = "gaga730"
        DOCKER_PASS = "gagana2005"
        IMAGE_NAME  = "student-course-registration"
        BUILD_TAG   = "${BUILD_NUMBER}"

        // AKS
        RESOURCE_GROUP  = "student-rg"
        CLUSTER_NAME    = "student-aks"
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
                withCredentials([
                    string(credentialsId: 'AZURE_APP_ID', variable: 'CLIENT_ID'),
                    string(credentialsId: 'AZURE_CLIENT_SECRET', variable: 'CLIENT_SECRET'),
                    string(credentialsId: 'AZURE_TENANT_ID', variable: 'TENANT_ID'),
                    string(credentialsId: 'AZURE_SUBSCRPTION_ID', variable: 'SUBSCRIPTION_ID')
                ]) {
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

        stage('Deploy to AKS') {
            steps {
                bat """
                echo Deploying application and Jenkins to AKS...

                kubectl apply -f mysql-deployment.yml
                kubectl apply -f mysql-service.yml
                kubectl apply -f deployment.yml
                kubectl apply -f service.yml

                echo Deploying Jenkins...
                kubectl apply -f jenkins-deployment.yml
                kubectl apply -f jenkins-service.yml

                echo Checking rollout status...
                kubectl rollout status deployment/student-course-registration-deployment
                kubectl rollout status deployment/jenkins-deployment
                
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
