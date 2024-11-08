from unittest import TestCase
from .consulta_cnpj_pedido import PedidoConsultaCNPJ
from .tipos_comuns import Cabecalho, CPFCNPJRemetente
from abstra_notas.assinatura import Assinador, gerar_pfx_teste
from lxml.etree import XMLSchema
from pathlib import Path
from tempfile import NamedTemporaryFile


class TestConsultaCnpjPedido(TestCase):
    def test_xml(self):
        pedido = PedidoConsultaCNPJ(
            cabecalho=Cabecalho(
                cpf_cnpj_remetente=CPFCNPJRemetente(
                    tipo="CNPJ", numero="99999997000100"
                )
            ),
            cnpj_contribuinte="60.701.190/0001-04",
        )

        schema = XMLSchema(
            file=Path(__file__).parent / "xsds" / "PedidoConsultaCNPJ_v01.xsd"
        )
        xml = pedido.gerar_xml()
        with NamedTemporaryFile() as f:
            pfx_path = Path(f.name)
            password = "123456"
            gerar_pfx_teste(path=pfx_path, password=password)
            xml_assinado = Assinador(pfx_path=pfx_path, pfx_password=password).assinar(
                xml
            )
            schema.assertValid(xml_assinado)
