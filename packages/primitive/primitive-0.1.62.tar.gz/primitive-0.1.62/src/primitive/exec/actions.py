import tempfile
import typing

from primitive.exec.interactive import interactive_shell

if typing.TYPE_CHECKING:
    pass


from paramiko import SSHClient

from primitive.utils.actions import BaseAction


class Exec(BaseAction):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def execute_command(self, hardware_identifier: str, command: str) -> None:
        hardware = self.primitive.hardware.get_hardware_from_slug_or_id(
            hardware_identifier=hardware_identifier
        )

        # since we found hardware, we need to check that the user:
        # - has a valid reservation on it
        # - OR if the device is free we can reserve it

        # if we create a reservation on behalf of the user, we need to release it after
        created_reservation_on_behalf_of_user = False

        if active_reservation := hardware["activeReservation"]:
            active_reservation_id = active_reservation["id"]
            reservation_result = self.primitive.reservations.get_reservation(
                reservation_id=active_reservation_id
            )
            reservation = reservation_result.data["reservation"]
        else:
            reservation_result = self.primitive.reservations.create_reservation(
                requested_hardware_ids=[hardware["id"]],
                reason="Executing command from Primitive CLI",
            )
            reservation = reservation_result.data["reservationCreate"]
            created_reservation_on_behalf_of_user = True

        reservation = self.primitive.reservations.wait_for_reservation_status(
            reservation_id=reservation["id"], desired_status="in_progress"
        )

        ssh_credentials = self.primitive.hardware.get_hardware_ssh_credentials(
            hardware_id=hardware["id"]
        )

        ssh_hostname = ssh_credentials["ssh_hostname"]
        ssh_username = ssh_credentials["ssh_username"]
        ssh_password = ssh_credentials["ssh_password"]
        ssh_private_key = ssh_credentials["ssh_private_key"]

        ssh_client = SSHClient()
        ssh_client.load_system_host_keys()
        keyfile = None
        if ssh_private_key:
            keyfile = tempfile.NamedTemporaryFile()
            keyfile.write(ssh_private_key.encode())
            keyfile.flush()
            ssh_client.connect(
                hostname=ssh_hostname,
                username=ssh_username,
                key_filename=keyfile.name,
            )
        else:
            ssh_client.connect(
                hostname=ssh_hostname,
                username=ssh_username,
                pkey=ssh_private_key,
                password=ssh_password,
            )

        if command:
            formatted_command = " ".join(command)
            stdin, stdout, stderr = ssh_client.exec_command(formatted_command)
            print(stdout.read())
            ssh_client.close()
        else:
            channel = ssh_client.get_transport().open_session()
            channel.get_pty()
            channel.invoke_shell()
            interactive_shell(channel)
            ssh_client.close()
            if keyfile:
                keyfile.close()

        if created_reservation_on_behalf_of_user:
            print("Cleaning up reservation.")
            self.primitive.reservations.release_reservation(
                reservation_or_hardware_identifier=reservation["id"]
            )
