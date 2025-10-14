pipeline {
  agent any

  environment {
    DOCKER_IMAGE = "gaga730/student-course-registration:latest"
    DOCKER_USER = "gaga730"
    DOCKER_PASS = "gagana2005"
    KUBECONFIG = credentials('kubeconfig-cred-gagana') // Jenkins credential for kubeconfig
  }

  stages {
    stage('Build Docker Image') {
      steps {
        bat "docker build -t %DOCKER_IMAGE% ."
      }
    }

    stage('Push Docker Image') {
      steps {
        bat "echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin"
        bat "docker push %DOCKER_IMAGE%"
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        bat "kubectl apply -f deployment.yaml"
        bat "kubectl apply -f service.yaml"
      }
    }

    stage('Verify Deployment') {
      steps {
        bat "kubectl get pods"
        bat "kubectl get svc"
      }
    }
  }

  post {
    success {
      echo 'Docker image built, pushed, and deployed to Kubernetes successfully!'
    }
    failure {
      echo 'Pipeline failed. Check logs for details.'
    }
  }
}