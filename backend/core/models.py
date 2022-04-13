from dataclasses import dataclass
from typing import Optional
from django.db import models
from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from utils import string_contains_array


class Network(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    uid = models.CharField(max_length=200)
    nome = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.uid} - {self.nome}"


class Station(models.Model):
    uid = models.CharField(max_length=200)
    codigo = models.CharField(max_length=200)
    nome = models.CharField(max_length=200)
    altitude = models.CharField(max_length=200, null=True)
    latitude = models.CharField(max_length=200, null=True)
    longitude = models.CharField(max_length=200, null=True)
    coord_x = models.CharField(max_length=200, null=True)
    coord_y = models.CharField(max_length=200, null=True)
    bacia = models.CharField(max_length=200, null=True)
    distrito = models.CharField(max_length=200, null=True)
    concelho = models.CharField(max_length=200, null=True)
    freguesia = models.CharField(max_length=200, null=True)
    entidade_responsavel_automatica = models.CharField(max_length=200, null=True)
    entidade_responsavel_convencional = models.CharField(max_length=200, null=True)
    tipo_estacao_automatica = models.CharField(max_length=200, null=True)
    tipo_estacao_convencional = models.CharField(max_length=200, null=True)
    entrada_funcionamento_convencional = models.CharField(max_length=200, null=True)
    entrada_funcionamento_automatica = models.CharField(max_length=200, null=True)
    encerramento_convencional = models.CharField(max_length=200, null=True)
    encerramento_automatica = models.CharField(max_length=200, null=True)
    telemetria = models.BooleanField(max_length=200, null=True)
    estado = models.CharField(max_length=200, null=True)
    indice_qualidade = models.CharField(max_length=200, null=True)

    network = models.ForeignKey(
        Network, on_delete=models.CASCADE, related_name="stations"
    )
    last_update = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f"{self.uid} - {self.nome}"


class Parameter(models.Model):
    @dataclass
    class FrequencyChoices:
        HOUR = "HOUR"
        MINUTE = "MINUTE"
        DAY = "DAY"
        MONTH = "MONTH"
        YEAR = "YEAR"

    uid = models.CharField(max_length=200)
    nome = models.CharField(max_length=200)

    @property
    def frequency(self) -> Optional[str]:
        if string_contains_array(self.name, ["anual"]):
            return Parameter.FrequencyChoices.YEAR
        elif string_contains_array(self.name, ["mensal"]):
            return Parameter.FrequencyChoices.MONTH
        elif string_contains_array(self.name, ["diario", "diaria"]):
            return Parameter.FrequencyChoices.DAY
        elif string_contains_array(self.name, ["horario", "horaria"]):
            return Parameter.FrequencyChoices.HOUR
        return None

    def __str__(self) -> str:
        return f"{self.uid} - {self.nome}"


class PSA(models.Model):
    station: Station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="psa"
    )
    parameter: Parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE, related_name="psa"
    )
    data_last_update = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f"{self.parameter.uid} - {self.station.uid}"

    class Meta:
        verbose_name = "Parameter Station Assignment"
        verbose_name_plural = "Parameter Station Assignments"


class Data(models.Model):
    timestamp = models.DateTimeField()
    value = models.FloatField()
    psa = models.ForeignKey(PSA, on_delete=models.CASCADE, related_name="data")

    def __str__(self) -> str:
        return f"{self.timestamp} - {self.value}"
