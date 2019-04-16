import random
from collections import defaultdict


class UniqueError(Exception):
    pass


class VmRow:
    def __init__(self, name, id_=None):
        self.name = name
        if not id_:
            id_ = random.randint(1, 2 ** 16)
        self.id = id_

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return self.id

    def __repr__(self):
        return str(self)


class VolumeRow:
    def __init__(self, size, id_=None):
        self.size = size
        if not id_:
            id_ = random.randint(1, 2 ** 16)
        self.id = id_

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return self.id

    def __repr__(self):
        return str(self.id)


class VmVolumeMappingRow:
    def __init__(self, vm: VmRow, volume: VolumeRow, deleted):
        self.vm = vm
        self.volume = volume
        self.deleted = deleted

    def __hash__(self):
        return hash(self.vm) + hash(self.volume) + hash(self.deleted)

    def __str__(self):
        return f"{self.vm.id} : {self.volume.id} : {self.deleted}"

    def __repr__(self):
        return self.__str__()


class InMemoryDBVmVolumeMappingTable:
    _size = 10
    _count = 0
    _slots = []
    # table maps
    _uniq_idx = set()
    _vm_id_idx = defaultdict(set)
    _volume_id_idx = defaultdict(set)

    # table vm
    _vmrows = defaultdict(set)

    # table volume
    _volumerows = defaultdict(set)

    def __init__(self):
        self._slots = [None for _ in range(self._size)]

    def _hash(self, h: int):
        slot_key = h % self._size
        return slot_key

    def put(self, item: VmVolumeMappingRow):
        original_hash = hash(item)

        if original_hash in self._uniq_idx:
            raise UniqueError("Такой обьект уже есть в базе")

        h = self._hash(original_hash)

        # use mutex
        try:
            self._slots[h] = item
            self._save_vms_map(h, item.vm.id)
            self._save_volume_map(h, item.volume.id)
            self._uniq_idx.add(original_hash)
        except Exception:
            raise

    def get_row(self, item: VmVolumeMappingRow):
        h = self._hash(hash(item))
        val = self._slots[h]
        return val

    def _save_vms_map(self, idx, vm_id):
        self._vm_id_idx[vm_id].add(idx)

    def _save_volume_map(self, idx, volume_id):
        self._volume_id_idx[volume_id].add(idx)

    def get_volume(self, vol_id):
        ret = self._volumerows[vol_id]
        return ret

    def get_vm(self, vm_id):
        ret = self._vmrows[vm_id]
        return ret

    def get_vms(self):
        ret = []
        for k in self._vmrows:
            ret.append({k: [self._slots[i] for i in self._vm_id_idx[k]]})
        return ret

    def get_volumes(self):
        ret = []
        for k in self._volumerows:
            ret.append({k: [self._slots[i] for i in self._volume_id_idx[k]]})
        return ret

    def save_vm(self, item: VmRow):
        self._vmrows[item.id] = item

    def save_volume(self, item: VolumeRow):
        self._volumerows[item.id] = item

    def mount(self, vol: VolumeRow, vm: VmRow):
        v = VmVolumeMappingRow(vm, vol, False)
        self.put(v)
        return v

    def unmount(self, vol: VolumeRow, vm: VmRow):
        for v in self._volume_id_idx[vol.id]:
            if self._slots[v].vm.id == vm.id:
                self._slots[v].deleted = True
                return self._slots[v]
