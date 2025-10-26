pipeline {
    agent any

    environment {
        DOCKER_USER = "gaga730"
        DOCKER_PASS = "gagana2005"
        IMAGE_NAME  = "student-course-registration"
        BUILD_TAG   = "${BUILD_NUMBER}"   // Jenkins build number (unique version)
        KUBECONFIG_PATH = "C:\\Users\\hello\\.kube\\config"  // Path to your local kubeconfig
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

        stage('Deploy to Local Kubernetes') {
            steps {
                bat """
                echo Deploying to Kubernetes cluster...
                set KUBECONFIG=%KUBECONFIG_PATH%

                REM  Update image in deployment (forces rolling update)
                kubectl set image deployment/student-course-registration-deployment student-course-registration=%DOCKER_USER%/%IMAGE_NAME%:%BUILD_TAG%

                REM  Ensure MySQL and services are running
                kubectl apply -f mysql-deployment.yaml
                kubectl apply -f mysql-service.yaml
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml

                REM  Wait for rollout to finish
                kubectl rollout status deployment/student-course-registration-deployment

                REM  Show current pod & service status
                kubectl get pods -o wide
                kubectl get svc
                """
            }
        }
    }

    post {
        success {
            echo "CI/CD pipeline completed successfully!"
            echo "Your website will be available through your NodePort + Cloudflare domain."
        }
        failure {
            echo "Pipeline failed. Please check Jenkins logs for details."
        }
    }
}