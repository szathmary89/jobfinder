
pipeline {
    agent any

    environment {
        PATH = "/home/szilvi/.nvm/versions/node/v26.13.1/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/bin"
    }

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
                sh 'node --version'
                sh 'npm --version'
            }
        }

        stage('Backend - Python compile') {
            steps {
                sh '''
                    python3 -m compileall -q backend/app
                '''
            }
        }

        stage('Frontend - Install') {
            steps {
                dir('frontend') {
                    sh 'npm ci'
                }
            }
        }

        stage('Frontend - Lint') {
            steps {
                dir('frontend') {
                    sh 'npm run lint'
                }
            }
        }

        stage('Frontend - Build') {
            steps {
                dir('frontend') {
                    sh 'npm run build'
                }
            }
        }
    }

    post {
        success {
            echo 'JobFinder CI: ALL CHECKS PASSED!'
        }
        failure {
            echo 'JobFinder CI: CHECKS FAILED!'
        }
    }
}
