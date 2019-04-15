from vms.views import VmsResource, VolumesResource, UnmountView, MountView

urls = [
    {'path': "/vms/", "view": VmsResource, "name": "vms"},
    {'path': "/volumes/", "view": VolumesResource, "name": "volumes"},
    {'path': "/unmount/<volume_id>/<vm_id>/", "view": UnmountView, "name": "unmount"},
    {'path': "/mount/<volume_id>/<vm_id>/", "view": MountView, "name": "mount"},
]
