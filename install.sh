#!/bin/bash

# Verificar si Python está instalado y su versión
python --version 2>&1 | grep -q "Python 3.9.7"

if [ $? -eq 0 ]; then
  echo "Python 3.9.7 está instalado."

  # Instalar las librerías desde requirements.txt
  pip install -r requirements.txt

  # Verificar si la instalación fue exitosa (método simple)
  if [ $? -eq 0 ]; then
    echo "Librerías instaladas correctamente."

    # Crear y ejecutar el script RunAsistente.sh
    touch RunAsistente.sh
    echo "#!/bin/bash" > RunAsistente.sh
    echo "python main.py 2>/dev/null" >> RunAsistente.sh
    chmod +x RunAsistente.sh
    ./RunAsistente.sh
  else
    echo "Error al instalar las librerías. Revisa requirements.txt y tu conexión a internet."
  fi
else
  echo "Python 3.9.7 no está instalado o la versión es incorrecta."
fi