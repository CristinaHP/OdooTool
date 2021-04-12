# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import Response
import json


class NominaController(http.Controller):
    @http.route('/api/nominas', auth='public', method=['GET'], csrf=False)
    def get_nominas(self, **kw):
        try:
            nominas = http.request.env['nueva_herramienta.nomina'].sudo().search_read([], ['id', 'nombreEmpresa', 'cif', 'nombreTrabajador', 'nif', 'numAfiliacion',
                                                                                           'mes', 'anio', 'salarioBase', 'totalDevengado', 'totalDeducciones', 'salarioNeto'])
            res = json.dumps(nominas, ensure_ascii=False).encode('utf-8')
            return Response(res, content_type='application/json;charset=utf-8', status=200)
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), content_type='application/json;charset=utf-8', status=505)

