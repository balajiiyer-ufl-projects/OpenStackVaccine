from novaclient.v1_1 import client
from client import Client
class OS_Client(Client):
    def __init__(self, menaces, processes, os_auth_info):
        Client.__init__(self, menaces, processes)
        self.handle = client.Client(os_auth_info["username"],
                                       os_auth_info["password"],
                                       os_auth_info["tenant_name"],
                                       os_auth_info["auth_url"],
                                       insecure=True,
                                       service_type="compute")

        for inst in self.handle.servers.list():
            self.id2inst[inst.id] = inst


    def kill_instance(self, instanceId):
        instance = self.get_instance(instanceId)

        if not "kill_instance" in self.menaces:
            raise Exception
        try:
            self._stop_instance(instanceId)
        except:
            self._pause_instance(instanceId)

    def kill_volume(self, instanceId, volume_id):
        volume = self.get_volume(instanceId, volume_id)
        assert volume != None
        self.handle.volumes.delete_server_volume(instanceId, volume.id)

    def list_instances(self):
        return self.handle.servers.list()

    def list_volumes(self, instanceId):
        pass

    def kill_process(self):
        pass

    def get_instance(self, instanceId, latest=False):
        assert instanceId != None
        instance = self.handle.servers.get(instanceId) if latest else self.id2inst.get(instanceId, None)
        if instance == None:
            raise Exception

        return instance

    def _start_instance(self, instanceId):
        instance = self.get_instance(instanceId)

        if (instance != None and
                instance.status != "ACTIVE"):
            instance.start()

    def _resume_instance(self, instanceId):
        instance = self.get_instance(instanceId)

        if (instance != None and
                instance.status != "ACTIVE"):
            instance.resume()

    def _stop_instance(self, instanceId):
        server = self.get_instance(instanceId)

        if (server != None and
                server.status == "ACTIVE"):
            server.stop();

    def _pause_instance(self, instanceId):
        server = self.get_instance(instanceId)

        if (server != None and
            server.status == "ACTIVE"):
            server.pause();

    def get_volume(self, instanceId, volume_id):
        instance_obj = self.id2inst.get(instanceId, None)
        if instance_obj == None:
            raise Exception

        volumes = self.handle.volumes.get_server_volumes(instanceId)

        for volume in volumes:
            if volume.volumeId == volume_id:
                return volume
        return None

    def _reattach_volume(self, volume):
        vol = self.handle.volumes.create_server_volume(
                server_id=volume.serverId,
                volume_id=volume.volumeId,
                device=volume.device)

