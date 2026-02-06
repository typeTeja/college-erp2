## Run Backend Server

cd apps/api
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

## Build Backend Server

pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

## Run Frontend Server

cd apps/web
npm run dev

## Build Frontend Server

npm run build

## Start Frontend Server

npm run start


pkill -9 -f "uvicorn app.main:app" || echo "Killed server"


taskkill /F /IM uvicorn.exe /T ; taskkill /F /IM python.exe /T