pipeline {
    agent any

    environment {
        DATA_SOURCE = 'mongo'
        DB_NAME = 'dashboard'

        ADMIN_PROFILE = 'C:\\Users\\Administrador.WIN-5UFR8AED4T8'
        PYTHON_HOME = 'C:\\Tools\\Python312'

        NODIST_HOME = 'C:\\Program Files (x86)\\Nodist'
    }

    stages {

        stage('Install Python 3.12') {
    steps {
        powershell '''
            $pythonDir = "C:\\Tools\\Python312"
            $pythonExe = "$pythonDir\\python.exe"

            if (Test-Path $pythonExe) {
                Write-Host "Python 3.12 ya esta instalado"
                & $pythonExe --version
                exit 0
            }

            Write-Host "Python 3.12 no encontrado. Instalando..."

            # Windows/PowerShell antiguo puede intentar TLS 1.0/1.1.
            # python.org requiere una negociacion TLS moderna.
            [Net.ServicePointManager]::SecurityProtocol = `
                [Net.SecurityProtocolType]::Tls12

            if (-not (Test-Path "C:\\Tools")) {
                New-Item `
                    -ItemType Directory `
                    -Path "C:\\Tools" `
                    -Force | Out-Null
            }

            $installer = "$env:TEMP\\python-3.12-installer.exe"

            Write-Host "Descargando instalador..."

            Invoke-WebRequest `
                -UseBasicParsing `
                -Uri "https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe" `
                -OutFile $installer

            if (-not (Test-Path $installer)) {
                throw "No se pudo descargar Python"
            }

            Write-Host "Instalando Python..."

            $process = Start-Process `
                -FilePath $installer `
                -ArgumentList @(
                    "/quiet",
                    "InstallAllUsers=1",
                    "TargetDir=$pythonDir",
                    "PrependPath=0",
                    "Include_test=0",
                    "Include_launcher=0"
                ) `
                -Wait `
                -PassThru

            if ($process.ExitCode -ne 0) {
                throw "Instalador Python fallo con codigo $($process.ExitCode)"
            }

            if (-not (Test-Path $pythonExe)) {
                throw "Python 3.12 no se instalo correctamente"
            }

            Write-Host "Python instalado:"
            & $pythonExe --version

            Remove-Item `
                $installer `
                -Force `
                -ErrorAction SilentlyContinue
        '''
    }
}

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

                    if exist .venv (
                rmdir /S /Q .venv
            )
                    if not exist .venv (
                        python -m venv .venv
                    )
                    .venv\\Scripts\\python.exe --version
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