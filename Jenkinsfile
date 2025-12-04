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
                sh "docker build -t ${IMAGE}:$GIT_COMMIT ."
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
                    sh "docker tag ${IMAGE}:$GIT_COMMIT ${IMAGE}:latest"
                    sh "docker push ${IMAGE}:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Apply Postgres PVC and DB manifests
                sh "kubectl apply -f ${K8S_MANIFEST_DIR}/pvc-postgres.yaml || true"
                sh "kubectl apply -f ${K8S_MANIFEST_DIR}/db-deployment.yaml || true"
                sh "kubectl apply -f ${K8S_MANIFEST_DIR}/db-service.yaml || true"

                // Update web deployment image or apply if it doesn't exist
                sh """
                kubectl set image deployment/web-deployment web=${IMAGE}:$GIT_COMMIT --record || \
                kubectl apply -f ${K8S_MANIFEST_DIR}/web-deployment.yaml
                """

                // Apply web service
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
