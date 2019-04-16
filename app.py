from flask import Flask


def create_app():
    app = Flask(__name__,)
    from vms import create_module as vms_create_module
    vms_blueprint = vms_create_module()

    app.register_blueprint(vms_blueprint, url_prefix="/")

    db = fill_db()
    app.db = db
    return app


def fill_db():

    from db import InMemoryDBVmVolumeMappingTable, VmRow, VolumeRow, VmVolumeMappingRow

    indb = InMemoryDBVmVolumeMappingTable()

    vm1 = VmRow(**{
        "name": "vm1",
        "id_": "asdkljasdlasjd"
    })

    vm2 = VmRow(**{
        "name": "vm2",
        "id_": "dasljdljsadlaj"
    })

    vm3 = VmRow(**{
        "name": "vm3",
        "id_": "wqeoiqwueiowu"
    })

    vm4 = VmRow(**{
        "name": "vm4",
        "id_": "zxcmnzxmcnxzc"
    })

    vm5 = VmRow(**{
        "name": "vm5",
        "id_": "wklkljlasdks"
    })

    vl1 = VolumeRow(**{
        "id_": 1233,
        "size": 12
    })

    vl2 = VolumeRow(**{
        "id_": 1487,
        "size": 100
    })

    vl3 = VolumeRow(**{
        "id_": 1489,
        "size": 228
    })

    vl4 = VolumeRow(**{
        "id_": 1337,
        "size": 42
    })

    vl5 = VolumeRow(**{
        "id_": 1548,
        "size": 200
    })

    vmap1 = VmVolumeMappingRow(vm2, vl3, False)
    vmap2 = VmVolumeMappingRow(vm5, vl5, True)
    vmap3 = VmVolumeMappingRow(vm1, vl5, False)

    vm = [vm1, vm2, vm3, vm4, vm5]
    vl = [vl1, vl2, vl3, vl4, vl5]
    vmap = [vmap1, vmap2, vmap3]

    for v in vm:
        indb.save_vm(v)

    for v in vl:
        indb.save_volume(v)

    for v in vmap:
        indb.put(v)

    return indb
