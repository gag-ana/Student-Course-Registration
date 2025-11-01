pipeline {
    agent any

    environment {
        IMAGE_NAME      = "student-course-registration"
        RESOURCE_GROUP  = "Student-course-Registration-rg"
        CLUSTER_NAME    = "student-course-registration-aks"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                bat """
                echo Building Docker image...
                docker build -t gaga730/%IMAGE_NAME%:$BUILD_NUMBER .
                docker tag gaga730/%IMAGE_NAME%:$BUILD_NUMBER gaga730/%IMAGE_NAME%:latest
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'DOCKER_HUB_CREDS', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat """
                    echo Logging into Docker Hub...
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push $DOCKER_USER/%IMAGE_NAME%:$BUILD_NUMBER
                    docker push $DOCKER_USER/%IMAGE_NAME%:latest
                    """
                }
            }
        }

        stage('Login to Azure') {
            steps {
                withCredentials([
                    string(credentialsId: 'AZURE_CLIENT_ID', variable: 'AZURE_CLIENT_ID'),
                    string(credentialsId: 'AZURE_CLIENT_SECRET', variable: 'AZURE_CLIENT_SECRET'),
                    string(credentialsId: 'AZURE_TENANT_ID', variable: 'AZURE_TENANT_ID'),
                    string(credentialsId: 'AZURE_SUBSCRIPTION_ID', variable: 'AZURE_SUBSCRIPTION_ID')
                ]) {
                    bat """
                    echo Logging into Azure...
                    az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
                    az account set --subscription $AZURE_SUBSCRIPTION_ID
                    """
                }
            }
        }

        stage('Connect to AKS') {
            steps {
                bat """
                echo Fetching AKS credentials...
                az aks get-credentials --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME --overwrite-existing
                """
            }
        }

        stage('Deploy to AKS') {
            steps {
                bat """
                echo Deploying application to AKS...
                kubectl apply -f mysql-deployment.yaml
                kubectl apply -f mysql-service.yaml
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml

                kubectl rollout status deployment/student-course-registration-deployment
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