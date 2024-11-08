from .bases import Entity, Pool


class Cluster(Entity):
    pass


class ClusterPool(Pool[Cluster]):
    pass
