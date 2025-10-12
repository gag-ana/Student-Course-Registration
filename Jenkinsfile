pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "gaga70/Student-Course-Registration" // Docker image name
    }

    stages {
        stage('Checkout') {
            steps {
                echo ' Pulling code from GitHub...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo ' Building Docker image...'
                sh "docker build -t ${DOCKER_IMAGE}:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo ' Pushing image to Docker Hub...'
                withCredentials([string(credentialsId: 'gaga70', variable: 'DOCKER_PASS')]) {
                    sh "echo ${DOCKER_PASS} | docker login -u gaga70 --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo ' Deploying to Kubernetes...'
                withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG')]) {
                    sh "kubectl --kubeconfig=${KUBECONFIG} apply -f deployment.yaml"
                    sh "kubectl --kubeconfig=${KUBECONFIG} apply -f service.yaml"
                    sh "kubectl --kubeconfig=${KUBECONFIG} rollout status deployment/student-course-registration"
                }
            }
        }
    }

    post {
        success {

            echo ' Deployment Successful!'
        }
        failure {
            echo ' Deployment Failed!'
        }
    }
}