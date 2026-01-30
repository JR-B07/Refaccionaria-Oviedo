@echo off
echo ============================================
echo Agregando productos via API REST
echo ============================================

curl -X POST "http://localhost:8000/api/v1/productos" -H "Content-Type: application/json" -d "{\"codigo\":\"LS-T1126 HS\",\"nombre\":\"EMPAQUE DE PLOMO\",\"marca\":\"DC\",\"categoria\":\"FORD / MAZDA / MERCURY\",\"precio_compra\":45.00,\"precio_venta\":65.00,\"stock_minimo\":5}"

curl -X POST "http://localhost:8000/api/v1/productos" -H "Content-Type: application/json" -d "{\"codigo\":\"TF-214\",\"nombre\":\"EMPAQUE DE TRANSMISION\",\"marca\":\"DCA\",\"categoria\":\"TOYOTA, SCION, LEXUS\",\"precio_compra\":85.00,\"precio_venta\":120.00,\"stock_minimo\":3}"

curl -X POST "http://localhost:8000/api/v1/productos" -H "Content-Type: application/json" -d "{\"codigo\":\"B-9293\",\"nombre\":\"BOMBA DE AGUA\",\"marca\":\"BW AUTOMOTIVE\",\"categoria\":\"NISSAN\",\"precio_compra\":350.00,\"precio_venta\":495.00,\"stock_minimo\":2}"

curl -X POST "http://localhost:8000/api/v1/productos" -H "Content-Type: application/json" -d "{\"codigo\":\"HA-1190-1\",\"nombre\":\"TORNILLO DE CARROCERIA\",\"marca\":\"DORL\",\"categoria\":\"CHEVROLET\",\"precio_compra\":8.50,\"precio_venta\":15.00,\"stock_minimo\":50}"

curl -X POST "http://localhost:8000/api/v1/productos" -H "Content-Type: application/json" -d "{\"codigo\":\"BE-39570-VL\",\"nombre\":\"RETEN CIGUENAL\",\"marca\":\"TF VICTOR\",\"categoria\":\"NISSAN\",\"precio_compra\":65.00,\"precio_venta\":95.00,\"stock_minimo\":10}"

curl -X POST "http://localhost:8000/api/v1/productos" -H "Content-Type: application/json" -d "{\"codigo\":\"SE-T-R-0\",\"nombre\":\"SELLO DE SILICONE SHOCK\",\"marca\":\"TOWI\",\"categoria\":\"VW\",\"precio_compra\":25.00,\"precio_venta\":40.00,\"stock_minimo\":15}"

curl -X POST "http://localhost:8000/api/v1/productos" -H "Content-Type: application/json" -d "{\"codigo\":\"4BX7002 020\",\"nombre\":\"EMPAQUE DE BRIDA\",\"marca\":\"MAHLE\",\"categoria\":\"Universal\",\"precio_compra\":12.00,\"precio_venta\":22.00,\"stock_minimo\":20}"

curl -X POST "http://localhost:8000/api/v1/productos" -H "Content-Type: application/json" -d "{\"codigo\":\"CL-95\",\"nombre\":\"ABRAZAD CHECA\",\"marca\":\"TF MICUNI\",\"categoria\":\"VW\",\"precio_compra\":18.00,\"precio_venta\":30.00,\"stock_minimo\":25}"

curl -X POST "http://localhost:8000/api/v1/productos" -H "Content-Type: application/json" -d "{\"codigo\":\"NEZ-7430050-5M\",\"nombre\":\"DRENAJE CRILCA\",\"marca\":\"EBAO\",\"categoria\":\"CHEVROLET\",\"precio_compra\":55.00,\"precio_venta\":85.00,\"stock_minimo\":8}"

curl -X POST "http://localhost:8000/api/v1/productos" -H "Content-Type: application/json" -d "{\"codigo\":\"32017\",\"nombre\":\"AMORTIGUADORES\",\"marca\":\"KYB\",\"categoria\":\"DODGE\",\"precio_compra\":580.00,\"precio_venta\":850.00,\"stock_minimo\":4}"

echo.
echo ============================================
echo Productos agregados exitosamente!
echo ============================================
pause
