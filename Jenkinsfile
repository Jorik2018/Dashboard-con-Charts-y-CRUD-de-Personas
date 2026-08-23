pipeline {
    agent any

    environment {
        DATA_SOURCE = 'mongo'
        DB_NAME = 'dashboard'

        ADMIN_PROFILE = 'C:\\Users\\Administrador.WIN-5UFR8AED4T8'
        PYTHON_HOME = 'C:\\Users\\Administrador.WIN-5UFR8AED4T8\\AppData\\Local\\Programs\\Python\\Python310'

        NODIST_HOME = 'C:\\Program Files (x86)\\Nodist'
    }

    stages {

        stage('Check Environment') {
            steps {
                bat '''
                    echo ==============================
                    echo PYTHON
                    echo ==============================

                    SET PATH=%PYTHON_HOME%;%PYTHON_HOME%\\Scripts;%PATH%

                    python --version
                    python -m pip --version

                    echo ==============================
                    echo NODE
                    echo ==============================

                    SET NODE_PATH=%NODIST_HOME%\\bin\\node_modules;%NODE_PATH%
                    SET NODIST_PREFIX=%NODIST_HOME%
                    SET PATH=%NODIST_HOME%\\bin;%PATH%

                    nodist --version
                    node --version
                    npm --version

                    echo ==============================
                    echo GIT
                    echo ==============================

                    git --version
                '''
            }
        }

        stage('Prepare Python') {
            steps {
                bat '''
                    SET PATH=%PYTHON_HOME%;%PYTHON_HOME%\\Scripts;%PATH%

                    if not exist .venv (
                        python -m venv .venv
                    )

                    .venv\\Scripts\\python.exe -m pip install --upgrade pip
                    .venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Verify Reflex') {
            steps {
                bat '''
                    SET NODE_PATH=%NODIST_HOME%\\bin\\node_modules;%NODE_PATH%
                    SET NODIST_PREFIX=%NODIST_HOME%
                    SET PATH=%NODIST_HOME%\\bin;%PATH%

                    .venv\\Scripts\\reflex.exe --version
                '''
            }
        }

        stage('Verify Mongo Secret') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'dashboard-mongo-uri',
                        variable: 'MONGO_URI'
                    )
                ]) {
                    powershell '''
                        if ([string]::IsNullOrWhiteSpace($env:MONGO_URI)) {
                            throw "MONGO_URI no esta configurado"
                        }

                        Write-Host "MONGO_URI recibido correctamente"
                        Write-Host "Longitud: $($env:MONGO_URI.Length)"
                        Write-Host "DB_NAME=$env:DB_NAME"
                        Write-Host "DATA_SOURCE=$env:DATA_SOURCE"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Entorno listo para desplegar.'
        }

        failure {
            echo 'Fallo preparando el entorno.'
        }
    }
}