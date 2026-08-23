pipeline {
    agent any

    environment {
        DATA_SOURCE = 'mongo'
        DB_NAME = 'dashboard'
    }

    stages {
        stage('Check Environment') {
            steps {
                powershell '''
                    Write-Host "=== Python ==="
                    python --version

                    Write-Host "=== Pip ==="
                    python -m pip --version

                    Write-Host "=== Node ==="
                    node --version

                    Write-Host "=== NPM ==="
                    npm --version

                    Write-Host "=== Git ==="
                    git --version
                '''
            }
        }

        stage('Prepare Python') {
            steps {
                powershell '''
                    if (-not (Test-Path ".venv")) {
                        python -m venv .venv
                    }

                    .\\.venv\\Scripts\\python.exe -m pip install --upgrade pip
                    .\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Verify Reflex') {
            steps {
                powershell '''
                    .\\.venv\\Scripts\\reflex.exe --version
                '''
            }
        }

        stage('Verify Secrets') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'dashboard-mongo-uri',
                        variable: 'MONGO_URI'
                    )
                ]) {
                    powershell '''
                        if ([string]::IsNullOrWhiteSpace($env:MONGO_URI)) {
                            throw "MONGO_URI no disponible"
                        }

                        Write-Host "Mongo URI disponible correctamente"
                    '''
                }
            }
        }
    }
}