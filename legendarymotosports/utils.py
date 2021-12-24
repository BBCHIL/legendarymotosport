import os

from django.core.exceptions import SuspiciousFileOperation

def prepare_form_data(data):
    """
    Removes lists from request data, making it clear: 
    {key: ['value']} -> {key: 'value'}
    """
    return {k:v for k,v in data.items()}


def delete_files(instance):
    """
    Deletes non used files from system. 
    Used when delete cars, accounts etc. 
    """
    try:
        if instance.image:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)
    except SuspiciousFileOperation:
        """
        Default images lives in static, if you 
        try to delete it, it will raise error. 
        In other case unused image will be deleted.
        """
        pass