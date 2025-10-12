pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t gaga70/student-course-registration:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'gaga70', variable: 'DOCKER_PASS')]) {
                    sh "echo ${DOCKER_PASS} | docker login -u gaga70 --password-stdin"
                    sh "docker push gaga70/student-course-registration:latest"
                }
            }
        }

        // stage('Deploy to Kubernetes') {
        //     steps {
        //         echo 'Kubernetes deployment will be added later.'
        //     }
        // }
    }

    post {
        success {
            echo ' Pipeline completed successfully!'
        }
        failure {
            echo ' Pipeline failed. Check logs for details.'
        }
    }
}