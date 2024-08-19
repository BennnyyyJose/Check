pipeline {
    environment {
        registry = "benniyamjose/check"
        registryCredential = "Jenkinsdocker"
        dockerImage = ''
    }
    
    agent any
    
    stages {
        stage('Check for Secrets'){
            steps {
                sh "rm -rf trufflehog.json || true"
                sh "docker run dxa4481/trufflehog:latest --json https://github.com/BennnyyyJose/Check.git > trufflehog.json || true"
                sh "cat trufflehog.json"
            }
        }
        stage('Safety Check') {
            steps {
                script {
                    def safetyInstalled = sh(script: "/usr/bin/pip show safety", returnStatus: true) == 0
                    if (!safetyInstalled) {
                        sh "/usr/bin/pip install safety --break-system-packages"
                    }
                }
                sh "rm -rf safety.json || true"
                sh "if [ -f requirement.txt ]; then /usr/bin/safety check -r requirement.txt --json > safety.json || true; else echo 'No requirement.txt found, skipping safety check'; fi"
                sh "cat safety.json || true"
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
