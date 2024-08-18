pipeline {
    environment {
        registry = "benniyamjose/cyberfrat-devsecops"
        registryCredential = "Jenkinsdocker"
        dockerImage = ''
    }
    
    agent any
    
    stages {
        stage('Run TruffleHog Scan') {
            steps {
                sh "rm -rf trufflehog.json || true"
                sh 'docker run dxa4481/trufflehog --json https://github.com/BennnyyyJose/Check.git > trufflehog.json'
                sh 'cat trufflehog.json'
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
                    dockerImage = docker.build(registry + ":$BUILD_NUMBER")
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
                sh 'docker run -d benniyamjose/cyberfrat-devsecops:$BUILD_NUMBER'
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'trufflehog.json', allowEmptyArchive: true
        }
    }
}
