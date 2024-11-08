"""
Editor Functions
"""

def create_remote_development(self, channelId, organizationId=None, channelVersion=None):
    """
    Creates a remote development environment.

    This method initiates a remote development session on the specified channel, optionally within a given organization.
    If no organizationId is provided, it defaults to the organization associated with the current user.

    Parameters
    ----------
    channelId : str
        The ID of the channel to use for creating the remote development session.
    channelVersion : str, optional
        The version of the channel to use. If not provided, defaults to the latest version.
    organizationId : str, optional
        The ID of the organization where the session will be created. 
        If not provided, defaults to the user's organization.

    Returns
    -------
    str
        A message indicating that the session is being created, along with a link to access the session.

    Notes
    -----
    - This function checks if the user is logged out before proceeding.
    - Calls `ana_api.createRemoteDevelopment` to initiate the session.
    - Displays a warning message indicating that the feature is experimental.

    Example Output
    --------------
    ⚠️ Warning: This feature is very experimental. Use with caution! ⚠️
    🚀 Your environment will be available here shortly: 🔗 <editorUrl> 🌐
    """
    if self.check_logout():
        return
    if organizationId is None:
        organizationId = self.organization
    session = self.ana_api.createRemoteDevelopment(
        organizationId=organizationId, 
        channelId=channelId, 
        channelVersion=channelVersion
    )

    print(
        "\n⚠️ Warning: This feature is very experimental. Use with caution! ⚠️\n"
        f"🚀 Your environment will be available here shortly: "
        f"🔗 {session['editorUrl']} 🌐\n"
    )


def delete_remote_development(self, editorSessionId, organizationId=None):
    """
    Deletes a remote development session.

    This method removes a specific editor session, optionally within a given organization.
    If no organizationId is provided, it defaults to the organization associated with the current user.

    Parameters
    ----------
    editorSessionId : str
        The ID of the editor session to be deleted.
    organizationId : str, optional
        The ID of the organization where the editor session is running.
        If not provided, defaults to the user's organization.

    Returns
    -------
    dict
        A dictionary representing the result of the session deletion, or session details upon deletion.

    Notes
    -----
    - This function checks if the user is logged out before proceeding.
    - Calls `ana_api.deleteRemoteDevelopment` to perform the deletion.
    """
    if self.check_logout():
        return
    if organizationId is None:
        organizationId = self.organization
    session = self.ana_api.deleteRemoteDevelopment(organizationId=organizationId, editorSessionId=editorSessionId)
    return session

def list_remote_development(self, organizationId=None): 
    """Shows all the active development sessions in the organization.
    
    Parameters
    ----------
    organizationId : str
        The ID of the organization to list the active development sessions. 
        If not provided, defaults to the user's organization
    
    Returns
    -------
    list[dict]
        List of remote development environments running in the organization.
    """
    if self.check_logout():
        return

    if organizationId is None:
        organizationId = self.organization

    sessions = self.ana_api.listRemoteDevelopment(organizationId=organizationId)

    if not sessions:
        print("✨ No active development sessions found. Use `create_remote_development` to start a new session.")
        return
    
    # Print message based on the availability of active sessions
    print(f"\n🚧 Active Development Sessions in Organization {organizationId}:\n")

    for session in sessions:
        print(
            f"  🆔 {session['editorSessionId']}: "
            f"🔗 {session['editorUrl']} "
            f"📊 Status: {session['status']['state']}"
        )
    
def stop_remote_development(self, editorSessionId, organizationId=None):
    """
    Stops a remote development session.

    This method stops a specific editor session, optionally within a given organization.
    If no organizationId is provided, it defaults to the organization associated with the current user.

    Parameters
    ----------
    editorSessionId : str
        The ID of the editor session to be stopped.
    organizationId : str, optional
        The ID of the organization where the editor session is running.
        If not provided, defaults to the user's organization.

    Returns
    -------
    dict
        A dictionary representing the result of the session stop operation.

    Notes
    -----
    - This function checks if the user is logged out before proceeding.
    - Calls `ana_api.stopRemoteDevelopment` to stop the session.
    """
    if self.check_logout():
        return
    if organizationId is None:
        organizationId = self.organization
    session = self.ana_api.stopRemoteDevelopment(organizationId=organizationId, editorSessionId=editorSessionId)

    print(f"\n🛑 Stopping Development Session {editorSessionId}...\n")

def start_remote_development(self, editorSessionId, organizationId=None):
    """
    Starts a remote development session.

    This method starts a specific editor session, optionally within a given organization.
    If no organizationId is provided, it defaults to the organization associated with the current user.

    Parameters
    ----------
    editorSessionId : str
        The ID of the editor session to be started.
    organizationId : str, optional
        The ID of the organization where the editor session is running.
        If not provided, defaults to the user's organization.

    Returns
    -------
    dict
        A dictionary representing the result of the session start operation.

    Notes
    -----
    - This function checks if the user is logged out before proceeding.
    - Calls `ana_api.startRemoteDevelopment` to start the session.
    """
    if self.check_logout():
        return
    if organizationId is None:
        organizationId = self.organization

    print(f"\n🚀 Starting Development Session {editorSessionId}...\n")

    session = self.ana_api.startRemoteDevelopment(organizationId=organizationId, editorSessionId=editorSessionId)

    print(f"Session resuming, your sessions will resume here shortly:\n🔗 {session['editorUrl']} 🌐\n")
