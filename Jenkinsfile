pipeline {
    agent any

    environment {
        REGISTRY = 'docker.io'
        IMAGE = "must22765/devsolutions-web"
        K8S_MANIFEST_DIR = 'kubernetes'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/BSSE23027/project'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker --version || true'
                sh "docker build -t ${IMAGE}:$GIT_COMMIT ./app"
                sh "docker tag ${IMAGE}:$GIT_COMMIT ${IMAGE}:latest"
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_PASS'
                )]) {
                    sh "echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin"
                    sh "docker push ${IMAGE}:$GIT_COMMIT"
                    sh "docker push ${IMAGE}:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh "kubectl apply -f ${K8S_MANIFEST_DIR}/pvc-postgres.yaml || true"
                sh "kubectl apply -f ${K8S_MANIFEST_DIR}/db-deployment.yaml || true"
                sh "kubectl apply -f ${K8S_MANIFEST_DIR}/db-service.yaml || true"

                sh """
                kubectl set image deployment/web-deployment web=${IMAGE}:$GIT_COMMIT --record || \
                kubectl apply -f ${K8S_MANIFEST_DIR}/web-deployment.yaml
                """

                sh "kubectl apply -f ${K8S_MANIFEST_DIR}/web-service.yaml || true"
            }
        }
    }

    post {
        success {
            echo 'Pipeline finished successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}