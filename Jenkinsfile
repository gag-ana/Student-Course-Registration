pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "gaga730/Student-Course-Registration"
        DOCKER_TAG = "latest"
        DOCKER_USER = "gaga730"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %DOCKER_IMAGE%:%DOCKER_TAG% ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'gaga730', variable: 'DOCKER_PASS')]) {
                    bat '''
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                        docker push %DOCKER_IMAGE%:%DOCKER_TAG%
                    '''
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
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo ' Pipeline failed. Check logs for details.'
        }
    }
}