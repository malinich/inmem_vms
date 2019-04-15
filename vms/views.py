from collections import defaultdict

from flask import jsonify, make_response
from flask_apispec import MethodResource

from dbs import volumes, vms, volume_mounts
from helpers import get_volume_mount


class VmsResource(MethodResource):
    def get(self):
        current_volumes = defaultdict(list)
        for volume in volume_mounts:
            if volume['deleted']:
                continue
            current_volumes[volume['vm_id']].append(volume['volume_id'])

        current_vms = [{'name': vm['name'], 'volumes': current_volumes.get(vm['id'], [])} for vm in vms]
        return jsonify(current_vms)


class VolumesResource(MethodResource):
    def get(self):
        current_volumes = {volume['id']: {'vm_id': None, 'past_mounts': [], 'id': volume['id']} for volume in volumes}
        for volume_mount in volume_mounts:
            if volume_mount['deleted']:
                current_volumes[volume_mount['volume_id']]['past_mounts'].append(volume_mount['vm_id'])
            else:
                current_volumes[volume_mount['volume_id']]['vm_id'] = volume_mount['vm_id']

        return jsonify(current_volumes)


class UnmountView(MethodResource):
    def post(self, volume_id, vm_id):
        vol_id = int(volume_id)
        v_mount = get_volume_mount(vol_id, vm_id)
        if v_mount is None:
            response = make_response(jsonify({"error": "not mounted"}), 400)
            return response
        v_mount['deleted'] = True
        return jsonify(v_mount)


class MountView(MethodResource):
    def post(self, volume_id, vm_id):
        vol_id = int(volume_id)
        v_mount = get_volume_mount(vol_id, vm_id)
        if v_mount:
            response = make_response(jsonify({"error": "already mounted"}), 400)
            return response
        data = {'vm_id': vm_id, 'volume_id': vol_id, 'deleted': False}
        volume_mounts.append(data)
        return jsonify(data)
