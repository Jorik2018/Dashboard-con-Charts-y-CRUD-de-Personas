Para decirte exactamente cómo levantarlo en localhost, muéstrame el contenido de estos 3 archivos:

rxconfig.py
requirements.txt
Dentro de app/, el archivo Python principal. Expande esa carpeta y muéstrame qué contiene.

Mientras tanto, probablemente se levanta así desde PowerShell:

cd Dashboard-con-Charts-y-CRUD-de-Personas

python -m venv .venv o python3 -m venv .venv

.\.venv\Scripts\Activate.ps1
macos - . .venv/bin/activate

pip install -r requirements.txt

reflex run

Si PowerShell te bloquea la activación del entorno:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

y luego:

.\.venv\Scripts\Activate.ps1

Si todo está bien, reflex run normalmente te mostrará algo parecido a:

App running at: http://localhost:3000
Backend running at: http://localhost:8000

Pero no ejecutes cosas al azar todavía. Pásame rxconfig.py + requirements.txt y una captura de app/, y te digo los comandos exactos para ese proyecto, incluyendo si necesita variables de entorno, base de datos, migraciones, etc.

