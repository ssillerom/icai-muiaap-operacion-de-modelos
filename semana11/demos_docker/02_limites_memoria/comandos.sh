# Demo 2 · Límites de memoria (cgroups)
# Pedimos 512 MB con un límite de 256 MB -> el kernel mata el proceso (OOM)
docker run --name oom --memory=256m --memory-swap=256m python:3.11-slim \
  python -c "x = bytearray(512 * 1024 * 1024); print('no debería verse')"
echo $?            # bash: 137  (PowerShell: $LASTEXITCODE)
docker ps -a       # el contenedor "oom" aparece como Exited (137)

# Mismo comando con 1 GB de límite -> funciona
docker run --name ok --memory=1g python:3.11-slim \
  python -c "x = bytearray(512 * 1024 * 1024); print('512 MB reservados OK')"

# Consumo en vivo: lanzamos un contenedor que se queda 60 s dormido (Ctrl+C para salir de stats)
docker run -d --name vivo --memory=512m python:3.11-slim sleep 60
docker stats vivo

# Limpieza
docker rm -f oom ok vivo                 # -f fuerza el borrado aunque siga en marcha
