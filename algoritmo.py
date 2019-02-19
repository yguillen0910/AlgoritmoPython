"""
	Segmento de código que procesa transacciones de un período de tiempo

	Parámetros del método:
	start_date -- timestamp fecha inicio de un período 
	second -- timestamp fecha fin de un período 

	Returns: array lista de transacciones.

	autor: yguillen

	fecha de modificación: 18/02/2019
"""

@asyncio.coroutine
def get_transactions(self, start_date, end_date=None, **kwargs):
	dic, dic['transactions'] = {}, []
	# Se obtiene lista de identificadores de facturas que fueron divididas en un 
	# periodo de tiempo
	query = TRANSACTION_X_QUERY.format(start=start_date, end=end_date)
	transactions = yield from self.cnxn.async_run(query)

	if transactions:

		for transaction in transactions:
			children = []

			principal_transaction = transaction.numberTrans

			# Se obtiene lista de identificadores de las partes de una factura 
			query = TRANSACTION_XC_QUERY.format(principal_transaction=principal_transaction)
			children = yield from self.cnxn.async_run(query)

			if children:
				transactions_to_process = []
				for child in children:
					transactions_to_process.append(child.numberTrans)

				transactions_to_process.append(principal_transaction)
				transactions_to_process = list(set(transactions_to_process))
				invoices_ids = ','.join(["'{}'".format(str(x)) for x in transactions_to_process])
				invoices_query = "AND COMPLEMENT_TRANSACTION.numberTrans in ("+invoices_ids+")"
				
				#Se obtiene información relevante de facturas como prductos fechas, totales, entre otros
				query = TRANSACTION_QUERY.format(invoices=invoices_query,filter="")
				rows = yield from self.cnxn.async_run(query)
				
				# Se obtiene diccionanio que contiene por cada transacción sus productos asociados (rows)
				transactions_by_invoice = self.create_lists(rows, dic)

				transactions_number_by_invoice = {}

				for k, v in transactions_by_invoice.items():
					"""Esta variable contiene por cada factura la cantidad de productos asociados, ya que ,era necesario
						procesar las transacciones complemtarias ordenadas por cantidad de productos  de menor a mayor
						ya que esto me permitía descartar productos 'usados'  
					"""
					transactions_number_by_invoice[k] = len(v)

				#Se ordenan las transacciones por cantidad de rows para procesarlas
				cantidadesOrdenadas = sorted(transactions_number_by_invoice.items(), key=lambda x: (x[1], -x[0]))

				#Era necesario que la transacción principal fuera la última en procesarse
				for k, v in cantidadesOrdenadas:
					if k == int(principal_transaction):
						i = cantidadesOrdenadas.index((k,v))				
						p = cantidadesOrdenadas.pop(i)
						cantidadesOrdenadas.append(p)
						break
				dic['usedproducts'] = []
				for indice, item in cantidadesOrdenadas:
					#Se obtienen las transacciones complementarias con sus productos con el formato correcto para enviar al API
					# tomando en cuenta que la cantidada de productos corresponda correctamente a cada transacción
					dic = self.build_x_transactions(transactions_by_invoice[indice], dic, principal_transaction)

	query = TRANSACTION_QUERY.format(invoices="", start=start_date, end=end_date)
	rows = yield from self.cnxn.async_run(query)

	#Se agrega al diccionario las transacciones sin complementos del período seleccionado 
	dic = self.build_transactions(rows,dic)

	Authorize(dic['transactions'], 'transaction')
	
	#filtro facturas 
	dic['transactions'] = [x for x in dic['transactions'] if x['transaction']['total'] > 0]

	#retorno las transacciones con y sin complementos del período seleccionado.
	return dic['transactions']