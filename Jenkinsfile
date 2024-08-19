pipeline {
    environment {
        registry = "benniyamjose/check"
        registryCredential = "Jenkinsdocker"
        dockerImage = ''
    }
    
    agent any
    
    stages {
        stage('Check for Secrets') {
            steps {
                sh "rm -rf trufflehog.json || true"
                sh "docker run dxa4481/trufflehog:latest --json https://github.com/BennnyyyJose/Check.git > trufflehog.json || true"
                sh "cat trufflehog.json"
            }
        }
        stage('Safety Check') {
            steps {
                sh "docker run --rm -v \$(pwd):/app pyupio/safety safety check -r /app/requirements.txt --json > safety.json"
                sh "cat safety.json"
            }
        }   

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build registry + ":$BUILD_NUMBER"
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    docker.withRegistry('', registryCredential) {
                        dockerImage.push()
                    }
                }
            }
        }

        stage('Test Run') {
            steps {
                sh "docker run -d ${registry}:${BUILD_NUMBER}"
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'trufflehog.json', allowEmptyArchive: true
        }
    }
}
