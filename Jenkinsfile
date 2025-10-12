pipeline {
  agent any

  environment {
    DOCKER_IMAGE = "gaga730/student-course-registration:latest"
    KUBE_DEPLOY_YAML = "gagana-deployment.yaml"
    KUBE_SERVICE_YAML = "student-course-registration-service.yaml"
  }

  stages {
    stage('Build Docker Image') {
      steps {
        bat "docker build -t %DOCKER_IMAGE% ."
      }
    }

    stage('Push Docker Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'gaga730', passwordVariable: 'gagana2005')]) {
          bat "docker login -u %DOCKER_USER% -p %DOCKER_PASS%"
          bat "docker push %DOCKER_IMAGE%"
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        bat "kubectl apply -f %KUBE_DEPLOY_YAML%"
        bat "kubectl apply -f %KUBE_SERVICE_YAML%"
        bat "kubectl rollout status deployment/student-course-registration-deployment"
      }
    }
  }

  post {
    success {
      echo 'Pipeline completed successfully!'
    }
    failure {
      echo 'Pipeline failed. Check logs for details.'
    }
  }
}
