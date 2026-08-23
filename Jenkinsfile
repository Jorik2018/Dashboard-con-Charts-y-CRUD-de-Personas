pipeline {
    agent any

    stages {
        stage('Hola Mundo') {
            steps {
                echo 'Hola mundo desde Jenkins :D'
            }
        }

        stage('Mongo Secret') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'MONGO_URI',
                        variable: 'MONGO_URI'
                    )
                ]) {
                    powershell '''
                        Write-Host "MONGO_URI:"
                        Write-Host $env:MONGO_URI
                    '''
                }
            }
        }
    }
}