from flask import jsonify, make_response, current_app
from flask_apispec import MethodResource

from db import InMemoryDBVmVolumeMappingTable, VmVolumeMappingRow, VolumeRow, VmRow, UniqueError


class VmsResource(MethodResource):
    def get(self):
        db: InMemoryDBVmVolumeMappingTable = current_app.db
        vms_rows = db.get_vms()

        data = [{'name': k, 'volumes': [v.volume.id for v in vs]} for vr in vms_rows for k, vs in vr.items()]

        return jsonify(data)


class VolumesResource(MethodResource):
    def get(self):
        db: InMemoryDBVmVolumeMappingTable = current_app.db
        volumes_rows = db.get_volumes()

        def func(id_, volumes):
            ret = {'id': id_, 'vm_id': None, 'past_mounts': []}
            for v in volumes:
                if v.deleted:
                    ret['past_mounts'].append(v.vm.id)
                else:
                    ret['vm_id'] = v.vm.id
            return ret

        data = [func(k, v) for row in volumes_rows for k, v in row.items()]

        return jsonify(data)


class UnmountView(MethodResource):
    def post(self, volume_id, vm_id):
        volume_id = int(volume_id)

        db: InMemoryDBVmVolumeMappingTable = current_app.db
        volume: VolumeRow = db.get_volume(volume_id)
        vm: VmRow = db.get_vm(vm_id)

        v = db.unmount(volume, vm)

        if v is None:
            response = make_response(jsonify({"error": "not mounted"}), 400)
            return response

        data = {
            "id": v.volume.id,
            "vm_id": v.vm.id,
        }
        return jsonify(data)


class MountView(MethodResource):
    def post(self, volume_id, vm_id):
        volume_id = int(volume_id)

        db: InMemoryDBVmVolumeMappingTable = current_app.db
        volume: VolumeRow = db.get_volume(volume_id)
        vm: VmRow = db.get_vm(vm_id)

        try:
            v = db.mount(volume, vm)
        except UniqueError:
            response = make_response(jsonify({"error": "already mounted"}), 400)
            return response

        data = {
            "id": v.volume.id,
            "vm_id": v.vm.id,
        }
        return jsonify(data)
