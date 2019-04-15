from dbs import volume_mounts


def get_volume_mount(volume_id, vm_id):
    for volume_mount in volume_mounts:
        if volume_mount['deleted']:
            continue
        if volume_mount['volume_id'] == volume_id and volume_mount['vm_id'] == vm_id:
            return volume_mount
    return None
