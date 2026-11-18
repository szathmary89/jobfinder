
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'JobFinder source code checked out.'
            }
        }

        stage('Environment') {
            steps {
                sh 'java -version'
                sh 'python3 --version'
            }
        }

        stage('Build Info') {
            steps {
                echo 'JobFinder CI pipeline is running!'
            }
        }
    }
}
