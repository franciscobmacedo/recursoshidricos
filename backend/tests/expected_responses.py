from common import schemas

networks = [
    schemas.Network(id="458192970", nome="ETA"),
    schemas.Network(id="920123705", nome="Hidrométrica"),
]


stations = [
    schemas.Station.parse_obj(
        {
            "id": "1627743378",
            "codigo": "19B/01H",
            "nome": "A-DOS-CUNHADOS",
            "altitude": "14",
            "latitude": "39.152",
            "longitude": "-9.302",
            "coord_x": "98984.104",
            "coord_y": "243387.146",
            "bacia": "RIBEIRAS DO OESTE",
            "distrito": "LISBOA",
            "concelho": "TORRES VEDRAS",
            "freguesia": "A DOS CUNHADOS",
            "entidade_responsavel_automatica": "Autoridade Nacional da Água",
            "entidade_responsavel_convencional": "-",
            "tipo_estacao_automatica": "SENSOR DE NÍVEL",
            "tipo_estacao_convencional": "-",
            "entrada_funcionamento_convencional": None,
            "entrada_funcionamento_automatica": "15-02-2002",
            "encerramento_convencional": None,
            "encerramento_automatica": None,
            "telemetria": False,
            "estado": "SUSPENSA",
            "indice_qualidade": None,
        }
    ),
    schemas.Station.parse_obj(
        {
            "id": "1627743350",
            "codigo": "03J/02H",
            "nome": "ABELHEIRA CANAL (R.E.)",
            "altitude": "756",
            "latitude": "41.795",
            "longitude": "-7.969",
            "coord_x": "213607.36",
            "coord_y": "536212.241",
            "bacia": "C\u00c1VADO/RIBEIRAS COSTEIRAS",
            "distrito": "VILA REAL",
            "concelho": "MONTALEGRE",
            "freguesia": "OUTEIRO",
            "entidade_responsavel_automatica": None,
            "entidade_responsavel_convencional": "EDP",
            "tipo_estacao_automatica": None,
            "tipo_estacao_convencional": "Limnigráfica",
            "entrada_funcionamento_convencional": "21-12-1972",
            "entrada_funcionamento_automatica": None,
            "encerramento_convencional": None,
            "encerramento_automatica": None,
            "telemetria": False,
            "estado": "ATIVA",
            "indice_qualidade": None,
        }
    ),
    schemas.Station.parse_obj(
        {
            "id": "1627743352",
            "codigo": "17H/04H",
            "nome": "ABRANTES LOPO",
            "altitude": "25",
            "latitude": "39.452",
            "longitude": "-8.188",
            "coord_x": "195271",
            "coord_y": "275953.774",
            "bacia": "TEJO",
            "distrito": "SANTARÉM",
            "concelho": "ABRANTES",
            "freguesia": "ROSSIO AO SUL DO TEJO",
            "entidade_responsavel_automatica": None,
            "entidade_responsavel_convencional": "CCDR-LVT",
            "tipo_estacao_automatica": None,
            "tipo_estacao_convencional": "ESCALA",
            "entrada_funcionamento_convencional": "01-10-1911",
            "entrada_funcionamento_automatica": None,
            "encerramento_convencional": "30-11-1977",
            "encerramento_automatica": None,
            "telemetria": False,
            "estado": "EXTINTA",
            "indice_qualidade": None,
        }
    ),
]


parameters = [
    schemas.Parameter(id="1843", nome="Nível hidrométrico Instantâneo"),
    schemas.Parameter(id="436115734", nome="Nível instantâneo máximo anual"),
    schemas.Parameter(id="1845", nome="Nível médio diário"),
]


data = schemas.DataEntryList.parse_obj(
    [
        {"timestamp": "1980-01-01T00:00:00", "value": 851030.0},
        {"timestamp": "1980-02-01T00:00:00", "value": 678589.0},
        {"timestamp": "1980-03-01T00:00:00", "value": 744619.0},
        {"timestamp": "1980-04-01T00:00:00", "value": 740899.0},
        {"timestamp": "1980-05-01T00:00:00", "value": 491122.0},
        {"timestamp": "1980-06-01T00:00:00", "value": 338570.0},
    ]
)
