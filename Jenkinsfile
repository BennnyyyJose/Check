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
                script {
                    // Remove any existing trufflehog.json file
                    sh "rm -rf trufflehog.json || true"

                    // Run TruffleHog using Docker and save the output to trufflehog.json
                    sh '''
                        docker run dxa4481/trufflehog https://github.com/BennnyyyJose/Check.git  > trufflehog.json
                    '''
                    
                    // Display the contents of trufflehog.json
                    sh 'cat trufflehog.json'
                }
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
