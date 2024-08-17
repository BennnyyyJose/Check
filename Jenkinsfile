pipeline {
    environment {
        registry = "benniyamjose/cyberfrat-devsecops"
        registryCredential = "Jenkinsdocker"
        dockerImage = ''
    }
    
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run TruffleHog Scan') {
            steps {
                script {
                    // Use bash to activate the virtual environment and run TruffleHog
                    sh '''
                        bash -c "source /home/benny/code1/Check/trufflehog-env/bin/activate && trufflehog --json https://github.com/BennnyyyJose/Check.git > trufflehog.json"
                    '''
                }
            }
        }

        stage('Display TruffleHog Results') {
            steps {
                script {
                    // Display the contents of the trufflehog.json file
                    sh 'cat trufflehog.json'
                }
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
                    docker.withRegistry('', registryCredential ) {
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
