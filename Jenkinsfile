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
        
        stage('safety'){
            steps {
                sh "pipx install safety"
                // Adding the correct path to the PATH environment variable
                sh "export PATH=\$PATH:/root/.local/bin"
                sh "rm -rf safety.json || true"
                sh "safety check -r requirements.txt --json > safety.json || true"
                sh "cat safety.json"
            }
        }
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage(''SAST) {
            steps {
                sh "rm -rf bandit.json || true"
                sh "bandit -r -f=json -o=bandit.json ."
                sh "cat bandit.json"
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
            archiveArtifacts artifacts: 'trufflehog.json,safety.json', allowEmptyArchive: true
    }
}
}
