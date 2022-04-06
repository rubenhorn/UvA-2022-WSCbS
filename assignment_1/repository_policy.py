import repository_in_memory, repository_shelve, utils

def get_repository(app):
    if app is not None:
        if utils.get_config(app, 'EPHEMERAL'):
            return repository_in_memory
    return repository_shelve
