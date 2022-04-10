from django.db import models
from bulk_update_or_create import BulkUpdateOrCreateQuerySet


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

    def __str__(self) -> str:
        return f"{self.uid} - {self.nome}"


class Parameter(models.Model):

    uid = models.CharField(max_length=200)
    nome = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.uid} - {self.nome}"


# Parameter Station Assignment
class PSA(models.Model):
    station: Station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="psa"
    )
    parameter: Parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE, related_name="psa"
    )
    last_updated = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f"{self.station.uid} - {self.parameter.uid}"


class Data(models.Model):
    timestamp = models.DateTimeField()
    value = models.FloatField()
    psa = models.ForeignKey(PSA, on_delete=models.CASCADE, related_name="data")

    def __str__(self) -> str:
        return f"{self.timestamp} - {self.value}"
