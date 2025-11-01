pipeline {
    agent any

    stages {
        stage('Install System Dependencies') {
            steps {
                sh '''
                    apt-get update
                    apt-get install -y commends curl
                '''
            }
        }

        stage('Verify Installation') {
            steps {
                sh 'curl --version'
            }
        }
    }
}
