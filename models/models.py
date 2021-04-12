# -*- coding: utf-8 -*-

from odoo import models, fields, api

class nomina(models.Model):
    _name = 'nueva_herramienta.nomina'
    _description = 'Nómina'
    _rec_name = 'nombreTrabajador'



    #nombreEmpresa = fields.Char(string='Empresa', required=True, size=30)
    nombreEmpresa = fields.Many2one(string='Empresa', required=True, comodel_name='res.partner')
    domicilioEmpresa = fields.Text(string='Domicilio')
    cif = fields.Char(string='CIF', required=True, size=10)



    nombreTrabajador = fields.Char(string='Trabajador', required=True, size=30)
    nif = fields.Char(string='NIF', required=True, size=10)
    numAfiliacion = fields.Char(string='Núm. Afil. Seguridad Social', required=True, size=12)
    grupoProfesional = fields.Char(string='Grupo profesional', size=20)
    foto = fields.Binary(string='Foto')



    mes = fields.Selection([('E', 'Enero'), ('F', 'Febrero'), ('Mz', 'Marzo'), ('Ab', 'Abril'), ('My', 'Mayo'),
                            ('Jn', 'Junio'), ('Jl', 'Julio'), ('Ag', 'Agosto'), ('S', 'Septiembre'), ('O', 'Octubre'),
                            ('N', 'Noviembre'), ('D', 'Diciembre')], string='Mes', required=True)
    anio = fields.Char(string='Año', required=True, size=4)



    salarioBase = fields.Float(string='Salario base', required=True)
    complementosSalariales = fields.Float(string='Complementos salariales')
    horasExtra = fields.Float(string='Horas extraordinarias')
    complementosNoSalariales = fields.Float(string='Complementos no salariales')
    totalDevengado = fields.Float(string='Total devengado', compute='_calcular_total_devengado')

    @api.depends('salarioBase', 'complementosSalariales', 'horasExtra', 'complementosNoSalariales')
    def _calcular_total_devengado(self):
        for record in self:
            record.totalDevengado = record.salarioBase + record.complementosSalariales + record.horasExtra + record.complementosNoSalariales



    contingenciasComunes = fields.Float(string='Contingencias comunes', compute='_calcular_contingencias_comunes')
    desempleo = fields.Float(string='Desempleo', compute='_calcular_desempleo')
    formacionProfesional = fields.Float(string='Formación profesional', compute='_calcular_formacion_profesional')
    irpf = fields.Float(string='IRPF', compute='_calcular_irpf')
    totalDeducciones = fields.Float(string='Total a deducir', compute='_calcular_total_deducir')

    @api.depends('salarioBase', 'complementosSalariales')
    def _calcular_contingencias_comunes(self):
        for record in self:
            record.contingenciasComunes = (record.salarioBase + record.complementosSalariales) * 0.047

    @api.depends('salarioBase', 'complementosSalariales')
    def _calcular_desempleo(self):
        for record in self:
            record.desempleo = (record.salarioBase + record.complementosSalariales) * 0.0155

    @api.depends('salarioBase', 'complementosSalariales')
    def _calcular_formacion_profesional(self):
        for record in self:
            record.formacionProfesional = (record.salarioBase + record.complementosSalariales) * 0.001

    @api.depends('salarioBase', 'complementosSalariales', 'horasExtra')
    def _calcular_irpf(self):
        for record in self:
            record.irpf = (record.salarioBase + record.complementosSalariales + record.horasExtra) * 0.14

    @api.depends('contingenciasComunes', 'desempleo', 'formacionProfesional', 'irpf')
    def _calcular_total_deducir(self):
        for record in self:
            record.totalDeducciones = record.contingenciasComunes + record.desempleo + record.formacionProfesional + record.irpf



    salarioNeto = fields.Float(string='Líquido total a percibir', compute='_calcular_salario_neto')

    @api.depends('totalDevengado', 'totalDeducciones')
    def _calcular_salario_neto(self):
        for record in self:
            record.salarioNeto = record.totalDevengado - record.totalDeducciones



    fecha = fields.Date(string='Fecha', required=True)



    revisada = fields.Boolean(string='Nómina revisada')
    entregada = fields.Boolean(string='Nómina entregada')

    def toggle_revisada(self):
        self.revisada = True

    def toggle_entregada(self):
        self.entregada = True



    def borrar_nomina(self):
        id_nomina = self.id
        #id_nomina = self.env['nueva_herramienta.nomina'].search([('nombreTrabajador', '=', 'Pedro')])
        #print(id_nomina)
        registro_nomina = self.env['nueva_herramienta.nomina'].browse([id_nomina])
        #print(registro_nomina.nombreTrabajador)
        registro_nomina.unlink()



    def name_get(self):
        display_title = []
        for record in self:
            name = record.nombreTrabajador
            name += " ({})".format(record.mes)
            name += " ({})".format(record.anio)
            display_title.append((record.id, (name)))
        return display_title



    estado = fields.Selection([('borrador', 'Borrador'), ('confirmado', 'Confirmado'), ('enviado', 'Enviado')], required=True, default='borrador')

    def button_borrador(self):
        for record in self:
            record.estado = 'borrador'

    def button_confirmar(self):
        for record in self:
            record.estado = 'confirmado'

    def button_enviar(self):
        for record in self:
            record.estado = 'enviado'


class NominaReport(models.AbstractModel):
    _name = 'report.nueva_herramienta.report_nomina_card'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('nueva_herramienta.report_nomina_card')

        return {
            'doc_ids': docids,
            'doc_model': self.env['nueva_herramienta.nomina'],
            'docs': self.env['nueva_herramienta.nomina'].browse(docids)
        }