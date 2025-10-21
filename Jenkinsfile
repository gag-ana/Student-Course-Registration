pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "gaga730/student-course-registration:latest"
        DOCKER_USER = "gaga730"
        DOCKER_PASS = "gagana2005"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                bat "docker build -t %DOCKER_IMAGE% ."
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
    }

    post {
        success {
            echo ' Docker image built and pushed successfully!'
        }
        failure {
            echo ' Pipeline failed. Check logs for details.'
        }
    }
}