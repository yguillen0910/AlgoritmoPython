# AlgoritmoPython

El problema a solucionar:
	Ser requería obtener información de transacciones de ventas de una base de datos sql y enviarla a un API.
Incovenientes que se presentaron:
	Antes de siquiera realizar el código era necesario estudiar la base de datos del cliente en búsqueda de información asociada a tranasacciones de ventas,
	en esa búsqueda se encontró que existían transacciones que separaban en n piezas donde existía una estructura principal que indicaba la cantidad de productos 
	asociados a la venta, el problema era que no era posible distinguir entre estas facturas relacionadas cuál era la cantidad de productos correcta asociada a cada construcción , para ellos se contruyó un algoritmo que se encargaba de cubrir los siguientes pasos:
	1. Buscar las facturas pricipales que se dividieran en piezas
	2. Buscar las piezas en las que se dividían las facturas principales.
	3. Obtener la cantidad de productos totales a procesar que de verdad pertenecieran a la venta (en la facturas en general (principal y piezas) se consiguieron productos con cantidades en negativo que represeentaban productos anulados y además entre las facturas relacionadas se podían 'cancelar' productos entre ellos)
	4. Para solucionar el tema sobre cuál producto se debía tomar en cuenta en cada transacción las facturas te'nían que ser procesadas en un orden en particular que dependía de la cantidad de rows que existían en cada columna y además la transacción o factura principal siempre debía ser la última en procesarse.
	5. una vez que se conocía cuáles facturas y productos debían procesarse se procedía a crear los objetos que se envíaban al servidor (dentro de este proceso se validaba la cantidad de productos que debían existir en cada factura)
	6. Se debía continuar con el proceso normal de obtener las transacciones del período consultado para enviarlo al servidor por ende se unían ambas listas o diccionarios dependiendo de la configuración de datos.
	7. Se envíaba la información de transacciones completas (facturas divididas y facturas sin dividir) al servidor para que los datos pudieran ser presentados a través de una página web.


