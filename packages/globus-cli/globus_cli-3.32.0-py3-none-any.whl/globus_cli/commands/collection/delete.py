import uuid

from globus_cli.login_manager import LoginManager
from globus_cli.parsing import collection_id_arg, command
from globus_cli.termio import display


@command("delete", short_help="Delete an existing Collection.")
@collection_id_arg
@LoginManager.requires_login("transfer")
def collection_delete(login_manager: LoginManager, *, collection_id: uuid.UUID) -> None:
    """
    Delete an existing Collection. This requires the administrator role on the
    Endpoint.
    """
    gcs_client = login_manager.get_gcs_client(collection_id=collection_id)
    res = gcs_client.delete_collection(collection_id)
    display(res, text_mode=display.RAW, response_key="code")
