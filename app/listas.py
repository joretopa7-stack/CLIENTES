from app.modelos.facturas import Factura
from app.modelos.clientes import Cliente
from app.modelos.transacciones import Transaccion

#Base de datos en memoria
ListaClientes: list[Cliente] = []
ListaFacturas: list[Factura] = []
ListaTransacciones: list[Transaccion] = []